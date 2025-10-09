
from __future__ import annotations
import logging
from typing import Any, Dict
import aiohttp

from .const import API_BASE

_LOGGER = logging.getLogger(__name__)

DEFAULT_HEADERS = {
    "Accept": "application/json, text/plain, */*",
    "User-Agent": "HomeAssistant-PGE-Outages/0.9 (+https://homeassistant.local)",
}

class PGEApi:
    def __init__(self, session: aiohttp.ClientSession):
        self._session = session

    async def fetch(self, *, page: int = 0, size: int = 500, city_sym: str | None = None, street_sym: str | None = None,
                    **query: Any) -> Dict[str, Any]:
        params: Dict[str, Any] = {"page": page, "size": size}
        if city_sym and street_sym:
            params["type"] = "teryt"
            params["citySym"] = city_sym
            params["streetSym"] = street_sym
        else:
            return {"items": []}

        params.update({k: v for k, v in query.items() if v})

        try:
            timeout = aiohttp.ClientTimeout(total=15, connect=5)
            async with self._session.get(API_BASE, params=params, headers=DEFAULT_HEADERS, timeout=timeout) as resp:
                status = resp.status
                ct = resp.headers.get("Content-Type", "")
                text = await resp.text()
                if status >= 400:
                    _LOGGER.warning("HTTP %s from PGE endpoint; body starts: %r", status, text[:200])
                    return {"items": [], "error": f"HTTP {status}"}
                try:
                    data = await resp.json(content_type=None)
                except Exception as jerr:
                    _LOGGER.warning("Failed to parse JSON (CT=%s): %s; body starts: %r", ct, jerr, text[:200])
                    return {"items": [], "error": f"json_error: {jerr}"}
                return data if isinstance(data, dict) else {"items": data}
        except Exception as e:
            _LOGGER.warning("PGE API fetch failed: %s", e)
            return {"items": [], "error": str(e)}
