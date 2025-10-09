
from __future__ import annotations
import asyncio
import voluptuous as vol
from typing import List, Tuple
from aiohttp import ClientError, ClientTimeout
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.selector import selector

from .const import (
    DOMAIN,
    FALCON_BASE,
    CONF_CITY,
    CONF_STREET,
    CONF_CITY_SYM,
    CONF_STREET_SYM,
    CONF_CALENDAR_ENTITY,
    CONF_SCAN_INTERVAL,
    DEFAULT_SCAN_INTERVAL,
    CONF_CITY_LABEL,
    CONF_STREET_LABEL,
)

TIMEOUT = ClientTimeout(total=10, connect=5)
HEADERS = {"Accept": "application/json, text/plain, */*", "User-Agent": "HA-PGEDystrybucjaOutages/0.1.0"}

OPTIONS_SCHEMA = vol.Schema({
    vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): int,
})

def _strip_sym(label: str) -> str:
    pos = label.rfind(" [")
    return label[:pos] if pos != -1 and label.endswith("]") else label

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    def __init__(self):
        self._city_sym: str | None = None
        self._street_sym: str | None = None
        self._city_label: str | None = None
        self._street_label: str | None = None
        self._calendar_entity: str | None = None
        self._cand_cities: List[Tuple[str, str]] = []  # (label, sym)
        self._cand_streets: List[Tuple[str, str]] = []  # (label, sym)
        self._city_has_streets: bool | None = None

    async def _get_json(self, url: str, params: dict):
        session = async_get_clientsession(self.hass)
        async with session.get(url, params=params, headers=HEADERS, timeout=TIMEOUT) as resp:
            return await resp.json(content_type=None)

    async def _check_city_has_streets(self, city_sym: str) -> bool:
        """Return True if Falcon reports at least one street for the city.
        We call with empty name; if API returns a list with length > 0, consider it has streets.
        If API shape is unexpected, default to True (keep old behavior).
        """
        try:
            data = await self._get_json(f"{FALCON_BASE}/street", {"citySym": city_sym, "name": ""})
            return isinstance(data, list) and len(data) > 0
        except Exception:
            # On any error, assume streets exist to keep normal flow
            return True

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            city = (user_input.get(CONF_CITY) or "").strip()
            if city:
                try:
                    data = await self._get_json(f"{FALCON_BASE}/teryt-city", {"name": city})
                    if isinstance(data, list) and data:
                        if len(data) == 1:
                            c = data[0]
                            self._city_sym = str(c.get("citySym"))
                            self._city_label = f"{c.get('voivodeshipName')} / {c.get('countyName')} / {c.get('cityName')}"
                            self._city_has_streets = await self._check_city_has_streets(self._city_sym)
                            if self._city_has_streets:
                                return await self.async_step_street()
                            else:
                                # Skip street step, proceed to calendar
                                self._street_sym = None
                                self._street_label = ""
                                return await self.async_step_calendar()
                        else:
                            self._cand_cities = [
                                (f"{c.get('voivodeshipName')} / {c.get('countyName')} / {c.get('cityName')} [{c.get('citySym')}]", str(c.get('citySym')))
                                for c in data
                            ]
                            options = {sym: label for (label, sym) in self._cand_cities}
                            schema = vol.Schema({vol.Required(CONF_CITY_SYM): vol.In(options)})
                            return self.async_show_form(step_id="pick_city", data_schema=schema)
                    else:
                        errors[CONF_CITY] = "city_not_found"
                except (ClientError, asyncio.TimeoutError):
                    errors["base"] = "cannot_connect"
                except Exception:
                    errors["base"] = "unknown"
            else:
                errors[CONF_CITY] = "city_required"

        schema = vol.Schema({vol.Required(CONF_CITY): str})
        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)

    async def async_step_pick_city(self, user_input=None):
        if user_input is not None:
            sym = user_input.get(CONF_CITY_SYM)
            for (label, s) in self._cand_cities:
                if s == sym:
                    self._city_sym = s
                    self._city_label = _strip_sym(label)
                    self._city_has_streets = await self._check_city_has_streets(self._city_sym)
                    if self._city_has_streets:
                        return await self.async_step_street()
                    else:
                        self._street_sym = None
                        self._street_label = ""
                        return await self.async_step_calendar()
        return self.async_abort(reason="city_required")

    async def async_step_street(self, user_input=None):
        errors = {}
        # If a previous check determined there are no streets, skip
        if self._city_has_streets is False:
            self._street_sym = None
            self._street_label = ""
            return await self.async_step_calendar()

        if user_input is not None:
            street = (user_input.get(CONF_STREET) or "").strip()
            if street:
                try:
                    data = await self._get_json(f"{FALCON_BASE}/street", {"citySym": self._city_sym, "name": street})
                    if isinstance(data, list) and data:
                        if len(data) == 1:
                            s = data[0]
                            self._street_sym = str(s.get("symUl"))
                            self._street_label = s.get("name")
                            return await self.async_step_calendar()
                        else:
                            self._cand_streets = [(f"{s.get('name')} [{s.get('symUl')}]", str(s.get('symUl'))) for s in data]
                            options = {sym: label for (label, sym) in self._cand_streets}
                            schema = vol.Schema({vol.Required(CONF_STREET_SYM): vol.In(options)})
                            return self.async_show_form(step_id="pick_street", data_schema=schema)
                    else:
                        errors[CONF_STREET] = "street_not_found"
                except (ClientError, asyncio.TimeoutError):
                    errors["base"] = "cannot_connect"
                except Exception:
                    errors["base"] = "unknown"
            else:
                errors[CONF_STREET] = "street_required"

        schema = vol.Schema({vol.Required(CONF_STREET): str})
        return self.async_show_form(step_id="street", data_schema=schema, errors=errors)

    async def async_step_pick_street(self, user_input=None):
        if user_input is not None:
            sym = user_input.get(CONF_STREET_SYM)
            for (label, s) in self._cand_streets:
                if s == sym:
                    self._street_sym = s
                    self._street_label = _strip_sym(label)
                    return await self.async_step_calendar()
        return self.async_abort(reason="street_required")

    async def async_step_calendar(self, user_input=None):
        errors = {}
        if user_input is not None:
            cal = user_input.get(CONF_CALENDAR_ENTITY)
            if cal:
                unique_id = f"{self._city_sym}_{self._street_sym or 'ALL'}"
                await self.async_set_unique_id(unique_id)
                self._abort_if_unique_id_configured()

                data = {
                    CONF_CITY_SYM: self._city_sym,
                    CONF_STREET_SYM: self._street_sym,
                    CONF_CALENDAR_ENTITY: cal,
                    CONF_CITY_LABEL: self._city_label or "",
                    CONF_STREET_LABEL: self._street_label or "",
                }
                title = f"{self._city_label}{(', ' + self._street_label) if self._street_label else ''}".strip()
                return self.async_create_entry(title=title, data=data)
            else:
                errors[CONF_CALENDAR_ENTITY] = "calendar_required"

        schema = vol.Schema({vol.Required(CONF_CALENDAR_ENTITY): selector({"entity": {"domain": "calendar"}})})
        return self.async_show_form(step_id="calendar", data_schema=schema, errors=errors)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return OptionsFlowHandler(config_entry)

class OptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="Options", data=user_input)
        return self.async_show_form(step_id="init", data_schema=OPTIONS_SCHEMA)
