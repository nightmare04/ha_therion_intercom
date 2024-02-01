"""Therion intercom camera."""

from __future__ import annotations

from datetime import timedelta
import logging

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, HEADERS, URL, URL_DATA

_LOGGER = logging.getLogger(__name__)
UPDATE_INTERVAL = timedelta(seconds=15)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> bool:
    """Setup sensor balance from a config entry created in the integrations UI."""  # noqa: D401
    entry = hass.data[DOMAIN][entry.entry_id]
    session = async_get_clientsession(hass)
    async_add_entities([SensorBalance(session, entry)], update_before_add=True)
    return True


class SensorBalance(SensorEntity):
    """Therion intercom balance sensor."""

    _attr_name = "Balance"
    _attr_native_unit_of_measurement = "RUB"
    _attr_icon = "mdi:currency-rub"
    _attr_device_class = SensorDeviceClass.MONETARY
    _attr_state_class = SensorStateClass.TOTAL


    def __init__(self, session, config) -> None:
        """Init intercom balance."""
        super().__init__()
        self.api = session["api"]
        self.config = config
        self.session = session
        self.contract = {}

    @property
    def name(self) -> str:
        """Return name of Therion balance sensor."""
        return "Balance sensor"

    async def async_update(self):
        """Update balance."""
        data = await self.api.async_get_contract()
        self._attr_native_value = data["content"][0]["balance"] or "0"

    @property
    async def async_unique_id(self) -> str:
        """Return the unique ID of the sensor."""
        await self.async_get_contract()
        return self.last_contract["content"][0]["entrances"][0]["id"] + "balance"
