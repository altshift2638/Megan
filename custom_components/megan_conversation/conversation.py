from __future__ import annotations
from dataclasses import dataclass
from typing import Any
import aiohttp

from homeassistant.components.conversation import (
    AbstractConversationAgent,
    ConversationInput,
    ConversationResult,
)
from homeassistant.core import HomeAssistant
from .const import DOMAIN, DEFAULT_API

@dataclass
class MeganAgent(AbstractConversationAgent):
    hass: HomeAssistant

    @property
    def attribution(self) -> dict[str, Any]:
        api = self._api
        return {"name": "Megan (Local)", "url": api.replace("/chat","")}

    @property
    def supported_languages(self) -> list[str]:
        return ["en", "en-GB", "en-US"]

    @property
    def _api(self) -> str:
        return self.hass.data.get(DOMAIN, {}).get("api_url", DEFAULT_API)

    async def async_process(self, user_input: ConversationInput) -> ConversationResult:
        text = user_input.text or ""
        payload = {"message": text}
        async with aiohttp.ClientSession() as session:
            async with session.post(self._api, json=payload, timeout=60) as resp:
                data = await resp.json()
        speak = data.get("reply", "I didn't catch that.")
        return ConversationResult(response=speak)

async def async_get_agent(hass: HomeAssistant, config: dict[str, Any]) -> MeganAgent:
    return MeganAgent(hass)
