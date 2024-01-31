"""Init for therion intercom."""

import logging

from homeassistant import config_entries
from homeassistant.core import HomeAssistant

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, config_entry: config_entries.ConfigEntry
) -> bool:
    """Set up platform from a ConfigEntry."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][config_entry.entry_id] = config_entry.data

    # Forward the setup to the camera platform.
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(config_entry, "camera")
    )
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(config_entry, "button")
    )
    return True


async def async_remove_entry(hass: HomeAssistant, entry) -> None:
    """Handle removal of an entry."""
    await hass.config_entries.async_forward_entry_unload(entry, "camera")
    await hass.config_entries.async_forward_entry_unload(entry, "button")
