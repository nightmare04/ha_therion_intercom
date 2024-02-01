"""API from therion intercom."""

import aiohttp

from .const import HEADERS, URL, URL_CODE, URL_LOGIN


async def send_telephone(data) -> str:
    """Send telephone number to get code."""
    payload = {}
    headers = {}
    api_utl = URL + URL_CODE
    payload["phone"] = data["phone"]
    async with aiohttp.ClientSession() as session:
        async with session.post(
            api_utl, json=payload, headers=HEADERS, ssl=False
        ) as resp:
            headers["Cookie"] = resp.headers.get("Set-Cookie")
            print(resp.status)
            return headers["Cookie"]


async def get_token(data):
    """Send telephone and sms code to get token."""
    payload = {}
    api_url = URL + URL_LOGIN
    HEADERS["Cookie"] = data["Cookie"]
    payload["phone"] = data["phone"]
    payload["code"] = data["code"]
    async with aiohttp.ClientSession() as session:
        async with session.post(
            api_url, json=payload, headers=HEADERS, ssl=False
        ) as resp:
            print(resp.status)
            json_resp = await resp.json()
            token = "Bearer " + json_resp["accessToken"]
            return token
