
from __future__ import annotations
import logging
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.storage import Store

from .const import (
    DOMAIN,
    CONF_CITY_SYM,
    CONF_STREET_SYM,
    CONF_CALENDAR_ENTITY,
    ATTR_UPDATED_AT,
    ATTR_ITEMS,
    ATTR_MATCHED,
    STORAGE_VERSION,
    STORAGE_KEY,
)
from .api import PGEApi

_LOGGER = logging.getLogger(__name__)

@dataclass
class Outage:
    id: str
    city: str | None
    street: str | None
    start: datetime | None
    end: datetime | None
    status: str | None
    updated_at: datetime | None
    raw: Dict[str, Any]

def _parse_dt_aware(x: str | None) -> datetime | None:
    if not x:
        return None
    try:
        dt = datetime.fromisoformat(x.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except Exception:
        for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"):
            try:
                return datetime.strptime(x, fmt).replace(tzinfo=timezone.utc)
            except Exception:
                continue
    return None

class PGEOutageCoordinator(DataUpdateCoordinator[dict]):
    def __init__(self, hass: HomeAssistant, *, entry: ConfigEntry, scan_interval: timedelta):
        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=scan_interval)
        self.entry = entry
        self.api = PGEApi(async_get_clientsession(hass))
        self._store = Store(hass, STORAGE_VERSION, f"{STORAGE_KEY}_{entry.entry_id}")
        self._pushed_ids: set[str] = set()
        self._calendar_entity = entry.data.get(CONF_CALENDAR_ENTITY)

    async def _async_update_data(self) -> dict:
        if not self._pushed_ids:
            data = await self._store.async_load()
            if data and isinstance(data, dict):
                self._pushed_ids = set(data.get("ids", []))

        city_sym = self.entry.data.get(CONF_CITY_SYM)
        street_sym = self.entry.data.get(CONF_STREET_SYM)

        raw = await self.api.fetch(city_sym=city_sym, street_sym=street_sym)
        items = raw.get("items") or raw.get("content") or raw

        outages: List[Outage] = []
        raw_matched: List[Dict[str, Any]] = []

        if isinstance(items, list):
            for it in items:
                if it.get("revoked") is True or it.get("deleted") is True:
                    continue
                start_raw = it.get("startAt")
                end_raw = it.get("stopAt")

                outages.append(
                    Outage(
                        id=str(it.get("id") or it.get("uuid") or ""),
                        city=it.get("cityName"),
                        street=it.get("streetName"),
                        start=_parse_dt_aware(start_raw),
                        end=_parse_dt_aware(end_raw),
                        status=str(it.get("type")) if it.get("type") is not None else None,
                        updated_at=_parse_dt_aware(it.get("confirmedAt")),
                        raw=it,
                    )
                )
                raw_matched.append(it)

        # Calendar push (best-effort, dedupe by outage id)
        if self._calendar_entity:
            for it in raw_matched:
                if it.get("revoked") is True or it.get("deleted") is True:
                    continue
                start = _parse_dt_aware(it.get("startAt"))
                end = _parse_dt_aware(it.get("stopAt"))
                if not start or not end:
                    continue
                oid = str(it.get("id") or it.get("uuid") or "")
                if not oid or oid in self._pushed_ids:
                    continue
                try:
                    t = it.get("type")
                    if t == 2:
                        summary = "PGE Wyłączenie: Planowane"
                    elif t == 1:
                        summary = "PGE Wyłączenie: Awaria"
                    else:
                        summary = "PGE Wyłączenie: Planowane"
                    description = it.get("description") or ""
                    city = it.get("cityName") or ""
                    street = it.get("streetName") or ""
                    location = ", ".join([p for p in [city, street] if p])

                    svc_data = {
                        "entity_id": self._calendar_entity,
                        "summary": summary,
                        "description": description,
                        "start_date_time": start.isoformat(),
                        "end_date_time": end.isoformat(),
                    }
                    if location:
                        svc_data["location"] = location

                    await self.hass.services.async_call("calendar", "create_event", svc_data, blocking=False)
                    self._pushed_ids.add(oid)
                except Exception as err:
                    _LOGGER.warning("Failed to create calendar event for %s: %s", oid, err)

            await self._store.async_save({"ids": list(self._pushed_ids)})

        now = datetime.now(timezone.utc)
        upcoming = sorted([o for o in outages if o.start and o.start >= now], key=lambda o: o.start)
        next_planned = upcoming[0] if upcoming else None

        return {
            "updated_at": now.isoformat(),
            "matched": raw_matched,
            "items": [o.raw for o in outages],
            "next_start": next_planned.start.isoformat() if next_planned and next_planned.start else None,
            "next_end": next_planned.end.isoformat() if next_planned and next_planned.end else None,
            "next_city": next_planned.city if next_planned else None,
            "next_street": next_planned.street if next_planned else None,
            "count": len(raw_matched),
        }
