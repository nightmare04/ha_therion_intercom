"""Therion intercom camera."""

from __future__ import annotations

from datetime import timedelta
import logging

from homeassistant.components.camera import (
    Camera,
    CameraEntityDescription,
    CameraEntityFeature,
    StreamType,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, HEADERS, URL, URL_DATA
from .api import TherionApi

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(seconds=15)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> bool:
    """Setup camera from a config entry created in the integrations UI."""  # noqa: D401
    entry = hass.data[DOMAIN][entry.entry_id]
    session = async_get_clientsession(hass)
    async_add_entities([TherionIntercom(session, entry)], update_before_add=True)
    return True


class TherionIntercom(Camera):
    """Therion intercom camera."""

    _attr_supported_features = CameraEntityFeature.STREAM
    _attr_frontend_stream_type = StreamType.HLS
    _attr_motion_detection_enabled = False

    entity_description = CameraEntityDescription(
        key="camera",
        icon="mdi:doorbell-video",
        name="Intercom",
    )

    def __init__(self, session, config) -> None:
        """Init intercom camera."""
        super().__init__()
        self.api: TherionApi = config["api"]
        self.config = config
        self.session = session
        self.contract = {}

    @property
    def name(self) -> str:
        """Return name of Therion camera."""
        return "Therion Intercom Camera"

    async def async_camera_image(
        self, width: int | None = None, height: int | None = None
    ) -> bytes | None:
        """Get still image for intercom camera."""
        image = await self.api.async_get_still_image()
        return image

    async def stream_source(self) -> str | None:
        """Get stream link for intercom camera."""
        await self.api.async_get_contract()
        stream_link = self.contract["content"][0]["entrances"][0]["videoLink"]
        return stream_link

    async def async_update(self):
        """Update intercom camera."""
        await self.stream_source()

    @property
    def unique_id(self) -> str:
        """Return the unique ID of the sensor."""
        return self.contract["content"][0]["id"]

    @property
    def use_stream_for_stills(self) -> bool:
        """Use stream to generate stills."""
        return True
