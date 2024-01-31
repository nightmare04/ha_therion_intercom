"""Config flow for therion intercom."""
import voluptuous as vol
from homeassistant import config_entries
from .api import *
from .const import DOMAIN


class TherionConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):  # noqa: D101
    def __init__(self) -> None:
        super().__init__()
        self.data = {}

    async def async_step_user(self, user_input=None):  # noqa: D102
        data_schema = {vol.Required("phone"): str}
        if user_input is not None:
            self.data["phone"] = user_input["phone"]
            self.data["Cookie"] = await send_telephone(self.data)
            return await self.async_step_token()
        return self.async_show_form(step_id="user", data_schema=vol.Schema(data_schema))

    async def async_step_token(self, user_input=None):
        data_schema = {vol.Required("code"): str}
        if user_input is not None:
            self.data["code"] = user_input["code"]
            self.data["token"] = await get_token(self.data)
            return self.async_create_entry(title="Therion Intercom", data=self.data)

        return self.async_show_form(
            step_id="token", data_schema=vol.Schema(data_schema)
        )
