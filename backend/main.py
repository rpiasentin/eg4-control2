"""Simple FastAPI backend for EG4 Float Control demo"""
import asyncio, os, time, random
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="EG4 Float Control Demo")

# --- in‑memory state -------------------------------------------------------
CURRENT_ABSORB = 58.2
CURRENT_FLOAT  = 55.2
BATTERY_VOLTAGE = 56.0
ACTION_LOG = []  # list[dict] -> {"ts": float, "action": str}
VOLT_HISTORY = []  # list[tuple(ts, volts)]

SAMPLE_INTERVAL = 30  # seconds

class Voltages(BaseModel):
    absorb: float
    float: float

# --- helpers ---------------------------------------------------------------
def log(action: str):
    ACTION_LOG.append({"ts": time.time(), "action": action})
    # keep log length reasonable
    if len(ACTION_LOG) > 200:
        ACTION_LOG.pop(0)

async def sampler() -> None:
    """background task: synthesise battery voltage data"""
    while True:
        global BATTERY_VOLTAGE
        # Fake voltage swings ±0.15 V
        BATTERY_VOLTAGE += random.uniform(-0.15, 0.15)
        ts = time.time()
        VOLT_HISTORY.append((ts, BATTERY_VOLTAGE))
        # keep 24h (2880 samples *30s)
        if len(VOLT_HISTORY) > 2880:
            VOLT_HISTORY.pop(0)
        await asyncio.sleep(SAMPLE_INTERVAL)

@app.on_event("startup")
async def _startup():
    asyncio.create_task(sampler())
    log("backend started")

# --- API -------------------------------------------------------------------
@app.get("/api/status")
async def status():
    return {
        "battery_voltage": round(BATTERY_VOLTAGE, 2),
        "absorb_voltage": CURRENT_ABSORB,
        "float_voltage": CURRENT_FLOAT,
        "timestamp": time.time(),
    }

@app.get("/api/history")
async def history():
    # return last 24h
    return [{"t": ts, "v": v} for ts, v in VOLT_HISTORY]

@app.get("/api/actions")
async def actions():
    return ACTION_LOG

@app.post("/api/setpoints")
async def setpoints(v: Voltages):
    global CURRENT_ABSORB, CURRENT_FLOAT
    CURRENT_ABSORB = v.absorb
    CURRENT_FLOAT = v.float
    log(f"Set Absorb→{v.absorb}V, Float→{v.float}V")
    return {"status": "ok"}
