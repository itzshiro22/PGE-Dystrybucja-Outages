
from __future__ import annotations

DOMAIN = "pge_outages"
PLATFORMS = ["sensor"]

DEFAULT_SCAN_INTERVAL = 120  # minutes

API_BASE = "https://power-outage.gkpge.pl/api/power-outage"
FALCON_BASE = "https://falcon.gkpge.pl"

CONF_CITY = "city"
CONF_STREET = "street"
CONF_CITY_SYM = "city_sym"
CONF_STREET_SYM = "street_sym"
CONF_CALENDAR_ENTITY = "calendar_entity"
CONF_SCAN_INTERVAL = "scan_interval"

CONF_CITY_LABEL = "city_label"
CONF_STREET_LABEL = "street_label"

ATTR_UPDATED_AT = "updated_at"
ATTR_ITEMS = "items"
ATTR_MATCHED = "matched"

STORAGE_VERSION = 1
STORAGE_KEY = "pge_outages_pushed_ids"
