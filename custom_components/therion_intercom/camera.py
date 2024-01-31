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

_LOGGER = logging.getLogger(__name__)
UPDATE_INTERVAL = timedelta(seconds=15)


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
        self.config = config
        self.session = session
        self.last_conctract = {}

    @property
    def name(self) -> str:
        """Return name of Therion camera."""
        return "Therion Intercom Camera"

    async def async_camera_image(
        self, width: int | None = None, height: int | None = None
    ) -> bytes | None:
        """Get still image for intercom camera."""
        headers = HEADERS
        headers["Cookie"] = self.config["Cookie"]
        headers["Authorization"] = self.config["token"]
        still_url = self.last_conctract["content"][0]["entrances"][0]["snapshotLink"]
        async with self.session.get(still_url, headers=headers) as resp:
            image = await resp.read()
        return image

    async def async_get_contract(self):
        """Get contract info from API."""
        payload = {}
        headers = HEADERS
        headers["Cookie"] = self.config["Cookie"]
        headers["Authorization"] = self.config["token"]
        api_url = URL + URL_DATA
        async with self.session.get(api_url, json=payload, headers=headers) as resp:
            json_data = await resp.json()
            self.last_conctract = json_data
        return json_data

    async def stream_source(self) -> str | None:
        """Get stream link for intercom camera."""
        json_data = await self.async_get_contract()
        stream_link = json_data["content"][0]["entrances"][0]["videoLink"]
        return stream_link

    async def async_update(self):
        """Update intercom camera."""
        await self.stream_source()
        await self.async_get_contract()

    @property
    def unique_id(self) -> str:
        """Return the unique ID of the sensor."""
        return self.last_conctract["content"][0]["id"]

    @property
    def use_stream_for_stills(self) -> bool:
        """Whether or not to use stream to generate stills."""
        return True
