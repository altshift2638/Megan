# Megan All-In-One (Add-on + HACS)

This repository contains:
- **Home Assistant Add-on**: `megan_ai` — ChatGPT-powered backend with a web demo.
- **HACS Integration**: `custom_components/megan_conversation` — registers Megan as a Conversation Agent.

## Install (Add-on Store)
1. In Home Assistant: **Settings → Add-ons → Add-on Store → ⋮ → Repositories → Add** this repo URL.
2. Install **Megan AI (ChatGPT)**.
3. Open the add-on **Configuration** and paste your **OPENAI_API_KEY**.
4. Start the add-on. Test at `http://<HA_IP>:8000/demo`.

## Install (HACS)
1. In HACS: **Integrations → ⋮ → Custom repositories → Add** this repo URL (Category: Integration).
2. Install **Megan Conversation Agent**.
3. **Settings → Devices & Services → Add Integration → Megan Conversation Agent** (keep default API `http://homeassistant.local:8000/chat`).
4. **Settings → Voice Assistants → Default conversation agent → Megan (Local)**.

---

### Notes
- The add-on uses a **no-s6** image (`init: false`) to avoid PID1 errors.
- Persona text can be changed in add-on options.
