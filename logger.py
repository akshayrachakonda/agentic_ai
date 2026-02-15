from datetime import datetime
import os


LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)


def log_step(step: str):

    with open(f"{LOG_DIR}/reasoning.log", "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now()}] {step}\n")
