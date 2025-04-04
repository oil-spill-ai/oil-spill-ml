# ml/app/main.py

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import os
import shutil

from app.predict import predict_image

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        result_path = predict_image(file_path)
        return JSONResponse(content={"mask_path": result_path})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
