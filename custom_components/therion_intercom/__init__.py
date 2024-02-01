"""Init for therion intercom."""

from homeassistant import core, config_entries
from .const import DOMAIN
from .api import TherionApi
import logging

_LOGGER = logging.getLogger(__name__)
_all = (
    "camera",
    "button",
    "sensor"
)


async def async_setup_entry(
    hass: core.HomeAssistant, config_entry: config_entries.ConfigEntry
) -> bool:
    """Set up platform from a ConfigEntry."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][config_entry.entry_id] = config_entry.data

    # Forward the setup to the camera, button, sensor platform.
    for domain in _all:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(config_entry, domain)
        )
    return True


async def async_remove_entry(hass, entry) -> None:
    """Handle removal of an entry."""
    for domain in _all:
        await hass.config_entries.async_forward_entry_unload(entry, domain)