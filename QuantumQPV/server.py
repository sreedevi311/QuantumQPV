from fastapi import FastAPI
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import json
import asyncio
import random
import joblib
import pandas as pd

# Import your simulation
from main import simulate_live

app = FastAPI()

# ✅ Allow frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Serve static folder (for drone.png etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

# ✅ Serve index.html
@app.get("/", response_class=HTMLResponse)
def home():
    return Path("index.html").read_text()

# Load ML model once
model = joblib.load("qpv_ml_model.pkl")

label_map = {
    0: "SAFE",
    1: "INTERCEPT_ATTACK",
    2: "REPLAY_ATTACK"
}


@app.get("/stream")
async def stream_data():

    async def event_generator():
        while True:

            attack_strength = random.uniform(0, 0.5)

            results = simulate_live(
                noise_level=random.uniform(0.01, 0.1),
                loss_prob=random.uniform(0.05, 0.15),
                attack_strength=attack_strength,
                delay_offset=random.uniform(0, 5e-6)
            )

            test_input = pd.DataFrame([results])
            prediction = model.predict(test_input)[0]

            status = "normal" if prediction == 0 else "spoof"

            data = {
                "status": status,
                "qber": round(results["QBER"], 4),
                "detection_rate": round(results["Detection_Rate"], 4),
                "avg_delay": round(results["Avg_Delay"], 6),
                "delay_deviation": round(results["Delay_Deviation"], 6),
                "noise_probability": round(results["Noise_Probability"], 4),
                "loss_probability": round(results["Loss_Probability"], 4),
                "attack_type": label_map[prediction]
            }

            yield f"data: {json.dumps(data)}\n\n"

            await asyncio.sleep(2)   # ✅ use async sleep (NOT time.sleep)

    return StreamingResponse(event_generator(), media_type="text/event-stream")