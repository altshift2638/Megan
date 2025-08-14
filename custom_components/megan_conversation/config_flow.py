from __future__ import annotations
from typing import Any
import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN, DEFAULT_API

class MeganConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    async def async_step_user(self, user_input: dict[str, Any] | None = None):
        if user_input is not None:
            if self._async_current_entries():
                return self.async_abort(reason="single_instance_allowed")
            return self.async_create_entry(title="Megan Conversation Agent", data=user_input)
        schema = vol.Schema({ vol.Required("api_url", default=DEFAULT_API): str })
        return self.async_show_form(step_id="user", data_schema=schema)
