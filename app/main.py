from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from pathlib import Path
import shutil
import time

from app.predict import predict_image
from app.utils import log_request, log_result, get_stats, clear_tmp

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

        log_request(file.filename)

        start_time = time.time()
        job_output_dir = RESULT_DIR / "job_results"
        result_path = predict_image(input_path, job_output_dir)
        duration = time.time() - start_time

        log_result(file.filename, duration)

        # Удаляем исходный файл
        input_path.unlink(missing_ok=True)

        return FileResponse(result_path, media_type="image/jpeg", filename=file.filename)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/stats")
def stats():
    return get_stats()

@app.post("/clear-tmp")
def clear_tmp_endpoint():
    clear_tmp()
    return {"status": "tmp cleared"}