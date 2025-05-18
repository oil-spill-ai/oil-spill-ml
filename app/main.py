from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
import shutil
from app.predict import predict_image

app = FastAPI()

UPLOAD_DIR = Path("/tmp/uploads")
RESULT_DIR = Path("/tmp/results")

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
RESULT_DIR.mkdir(parents=True, exist_ok=True)

@app.post("/segment")
async def segment_image(file: UploadFile = File(...)):
    try:
        input_path = UPLOAD_DIR / file.filename
        with input_path.open("wb") as f:
            shutil.copyfileobj(file.file, f)

        job_output_dir = RESULT_DIR / "job_results"
        result_path = predict_image(input_path, job_output_dir)

        return FileResponse(result_path, media_type="image/jpeg", filename=file.filename)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
