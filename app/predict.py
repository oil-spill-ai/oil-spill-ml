from app.model import model
from pathlib import Path

def predict_image(input_path: Path, output_dir: Path, conf: float = 0.33) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)

    model(
        source=input_path,
        task="segment",
        save=True,
        conf=conf,
        imgsz=640,
        exist_ok=True,
        project=output_dir.parent,
        name=output_dir.name,
    )

    return output_dir / input_path.name
