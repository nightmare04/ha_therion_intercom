"""Therion intercom camera."""

from __future__ import annotations

from datetime import timedelta
import logging

from homeassistant.components.button import ButtonEntity, ButtonEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, HEADERS, URL, URL_DATA, URL_OPEN

_LOGGER = logging.getLogger(__name__)
UPDATE_INTERVAL = timedelta(seconds=15)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> bool:
    """Setup button from a config entry created in the integrations UI."""  # noqa: D401
    entry = hass.data[DOMAIN][entry.entry_id]
    session = async_get_clientsession(hass)
    async_add_entities([OpenButton(session, entry)], update_before_add=True)
    return True


class OpenButton(ButtonEntity):
    """Therion intercom open_button."""

    entity_description = ButtonEntityDescription(
        key="button",
        icon="mdi:lock-open",
        name="Open",
    )

    def __init__(self, session, config) -> None:
        """Init intercom camera."""
        super().__init__()
        self.config = config
        self.session = session
        self.last_contract = {}

    @property
    def name(self) -> str:
        """Return name of Therion open door button."""
        return "Open door button"

    async def async_get_contract(self):
        """Get contract info from API."""
        payload = {}
        headers = HEADERS
        headers["Cookie"] = self.config["Cookie"]
        headers["Authorization"] = self.config["token"]
        api_url = URL + URL_DATA
        async with self.session.get(api_url, json=payload, headers=headers) as resp:
            json_data = await resp.json()
            self.last_contract = json_data
        return json_data

    async def async_update(self):
        """Update intercom camera."""
        await self.async_get_contract()

    async def async_press(self):
        """Open intercom door."""
        url = (
            URL
            + URL_OPEN
            + self.last_contract["content"][0]["entrances"][0]["id"]
            + "/open"
        )
        payload = {}
        headers = HEADERS
        headers["Cookie"] = self.config["Cookie"]
        headers["Authorization"] = self.config["token"]
        async with self.session.post(url, json=payload, headers=headers) as resp:
            if resp.status == 200:
                return True
            else:
                return False

    @property
    def unique_id(self) -> str:
        """Return the unique ID of the sensor."""
        return self.last_contract["content"][0]["entrances"][0]["id"]
