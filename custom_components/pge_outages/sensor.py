
from __future__ import annotations
from datetime import datetime, timezone

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, ATTR_MATCHED, CONF_CITY_SYM, CONF_STREET_SYM, CONF_CITY_LABEL, CONF_STREET_LABEL
from .coordinator import PGEOutageCoordinator

def _parse_dt_aware(s: str | None):
    if not s:
        return None
    try:
        dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except Exception:
        for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"):
            try:
                return datetime.strptime(s, fmt).replace(tzinfo=timezone.utc)
            except Exception:
                continue
    return None

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    coord: PGEOutageCoordinator = hass.data[DOMAIN][entry.entry_id]
    city_label = entry.data.get(CONF_CITY_LABEL) or entry.data.get(CONF_CITY_SYM) or ""
    street_label = entry.data.get(CONF_STREET_LABEL) or entry.data.get(CONF_STREET_SYM) or ""
    suffix = f" – {city_label}, {street_label}" if city_label or street_label else ""
    async_add_entities([PGEOutageNextHoursSensor(coord, entry, suffix)])

class PGEOutageNextHoursSensor(CoordinatorEntity[PGEOutageCoordinator], SensorEntity):
    _attr_icon = "mdi:calendar-clock"
    _attr_native_unit_of_measurement = "h"

    def __init__(self, coordinator: PGEOutageCoordinator, entry: ConfigEntry, name_suffix: str):
        super().__init__(coordinator)
        city_sym = entry.data.get(CONF_CITY_SYM) or "city"
        street_sym = entry.data.get(CONF_STREET_SYM) or "street"
        city_label = (entry.data.get(CONF_CITY_LABEL) or "").replace(" ", "_").lower()
        street_label = (entry.data.get(CONF_STREET_LABEL) or "").replace(" ", "_").lower()
        self._attr_name = f"Wyłączenia PGE Dystrybucja{name_suffix}"
        self._attr_unique_id = f"pge_next_hours_{city_sym}_{street_sym}_{city_label}_{street_label}"

    def _all_items(self):
        data = self.coordinator.data or {}
        items = data.get(ATTR_MATCHED) or []
        return [it for it in items if not it.get("revoked") and not it.get("deleted")]

    @property
    def _next_future_item(self):
        now = datetime.now(timezone.utc)
        future = []
        for it in self._all_items():
            start = _parse_dt_aware(it.get("startAt"))
            if start and start >= now:
                future.append((start, it))
        if not future:
            return None
        future.sort(key=lambda t: t[0])
        return future[0][1]

    @property
    def native_value(self):
        now = datetime.now(timezone.utc)
        it = self._next_future_item
        if not it:
            return 0
        start = _parse_dt_aware(it.get("startAt"))
        if not start:
            return 0
        delta_seconds = max(0.0, (start - now).total_seconds())
        hours = int(delta_seconds // 3600)
        return hours

    @property
    def extra_state_attributes(self):
        it = self._next_future_item
        if not it:
            return {
                "type": "none",
                "description": "No upcoming outages",
                "start": None,
                "stop": None,
                "confirmed_by_pge": None,
            }
        t = it.get("type")
        if t == 2:
            typ = "planned"
        elif t == 1:
            typ = "outage"
        else:
            typ = t if t is not None else "planned"
        return {
            "type": typ,
            "description": it.get("description"),
            "start": it.get("startAt"),
            "stop": it.get("stopAt"),
            "confirmed_by_pge": it.get("confirmedAt"),
        }
