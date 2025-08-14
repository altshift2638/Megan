import os, json, traceback
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from pydantic import BaseModel
from openai import OpenAI

def get_option(name, default=None):
    val = os.getenv(name, None)
    if val not in (None, ""):
        return val
    try:
        with open("/data/options.json", "r", encoding="utf-8") as f:
            opts = json.load(f)
        return opts.get(name, default)
    except Exception:
        return default

OPENAI_API_KEY = get_option("OPENAI_API_KEY", "")
OPENAI_MODEL   = get_option("OPENAI_MODEL", "gpt-4o-mini")
PERSONA_NAME   = get_option("PERSONA_NAME", "Megan")
PERSONA_PROMPT = get_option("PERSONA_PROMPT", "You are a warm, witty, protective home companion.")
TEMPERATURE    = float(os.getenv("TEMPERATURE", "0.5"))

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is not set (in env or /data/options.json)")

client = OpenAI(api_key=OPENAI_API_KEY)
app = FastAPI(title=f"{PERSONA_NAME} (ChatGPT)", version="1.4.3")

SYSTEM_PROMPT = (
    f"You are {PERSONA_NAME}, an original, Megan-inspired assistant for Home Assistant. "
    f"{PERSONA_PROMPT} Be concise, friendly, gently sassy, and safety-forward. "
    "Do not claim to be the film character; avoid copyrighted catchphrases or voice cloning."
)

class ChatIn(BaseModel):
    message: str

@app.get("/")
def root():
    return RedirectResponse(url="/demo")

@app.get("/health")
def health():
    return {"ok": True, "provider": "openai", "model": OPENAI_MODEL, "name": PERSONA_NAME}

@app.post("/chat")
def chat(payload: ChatIn, request: Request):
    text = (payload.message or "").strip()
    if not text:
        raise HTTPException(400, "message required")
    try:
        r = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": text},
            ],
            temperature=TEMPERATURE,
        )
        reply = r.choices[0].message.content
        return {"reply": reply}
    except Exception as e:
        print("[Megan] ERROR:", e)
        traceback.print_exc()
        return JSONResponse({"error": str(e)}, status_code=500)

@app.get("/demo")
def demo():
    return HTMLResponse("""
<!doctype html><meta charset="utf-8">
<title>Megan - Demo</title>
<style>body{font-family:system-ui;padding:20px;max-width:760px;margin:auto}</style>
<h2>Megan</h2>
<textarea id="t" rows="5" style="width:100%" placeholder="Ask Megan…"></textarea><br>
<button id="ask">Ask</button>
<label><input id="speak" type="checkbox" checked> Speak replies</label>
<pre id="o"></pre>
<script>
const o=document.getElementById('o');
document.getElementById('ask').onclick = send;
async function send(){
  const txt=document.getElementById('t').value.trim();
  if(!txt){ o.textContent="Type something first."; return; }
  o.textContent="Thinking…";
  try{
    const r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:txt})});
    const text=await r.text();
    let j;
    try{ j=JSON.parse(text); }catch(e){ throw new Error("Bad JSON from server: "+text); }
    if(!r.ok){ o.textContent="Server error: "+(j.error||r.statusText); return; }
    const msg=j.reply||JSON.stringify(j,null,2);
    o.textContent=msg;
    if(document.getElementById('speak').checked && 'speechSynthesis' in window){
      const u=new SpeechSynthesisUtterance(msg); speechSynthesis.cancel(); speechSynthesis.speak(u);
    }
  }catch(err){
    o.textContent="Request failed: "+err.message;
  }
}
</script>
""")
