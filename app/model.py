from ultralytics import YOLO
from pathlib import Path

# Загружаем модель один раз при старте
model_path = Path("weights") / "best.pt"
model = YOLO(model_path)
