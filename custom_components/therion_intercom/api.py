"""API from therion intercom."""

import aiohttp
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from .const import URL, URL_CODE, URL_DATA, URL_LOGIN, HEADERS


class TherionApi:
    def __init__(self):
        self.contract = None
        self.headers = HEADERS

    @classmethod
    async def create(cls, hass, config):
        self = cls
        self.hass = hass
        self.config = config
        self.session = async_get_clientsession(hass)
        self.contract = await self.async_get_contract()
        return self

    async def send_telephone(self, data, payload=None) -> None:
        """Send telephone number to get code."""
        headers = HEADERS
        api_utl = URL + URL_CODE
        payload["phone"] = data["phone"]
        async with self.session.post(api_utl, json=payload, headers=headers, ssl=False) as resp:
            data["Cookie"] = resp.headers.get("Set-Cookie")
            self.headers["Cookie"] = data["Cookie"]

    async def get_token(self, data, payload=None) -> None:
        """Send telephone and sms code to get token."""
        api_url = URL + URL_LOGIN
        payload["phone"] = data["phone"]
        payload["code"] = data["code"]
        async with self.session.post(
            api_url, json=payload, headers=self.headers, ssl=False
        ) as resp:
            print(resp.status)
            json_resp = await resp.json()
            data["token"] = "Bearer " + json_resp["accessToken"]

    async def async_get_contract(self, payload=None) -> None:
        self.headers["Cookie"] = self.config["Cookie"]
        self.headers["Authorization"] = self.config["token"]
        url = URL + URL_DATA
        async with self.session.get(url, json=payload, headers=headers) as resp:
            self.contract = await resp.json()

    async def async_get_still_image(self):
        still_url = self.contract["content"][0]["entrances"][0]["snapshotLink"]
        async with self.session.get(still_url, headers=self.headers) as resp:
            image = await resp.read()
            return image
