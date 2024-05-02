import io
import json
import os
import shutil
from contextlib import asynccontextmanager
from datetime import datetime, timedelta

import joblib
import librosa
import uvicorn
from fastapi import BackgroundTasks, FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from dsp import reverberation as rvb
from ml.predict import predict

DELAY_FOR_DELETION = timedelta(hours=1)
ml_param = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    os.makedirs(rvb.PROCESSED_FILES_DIRECTORY, exist_ok=True)
    ml_param["scaler"] = joblib.load("ml/scaler.gz")
    ml_param["model"] = joblib.load("ml/model.gz")
    yield
    shutil.rmtree(rvb.PROCESSED_FILES_DIRECTORY, ignore_errors=True)
    ml_param.clear()


app = FastAPI(lifespan=lifespan)
cache = {}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    expose_headers=["Content-Disposition"],
)


@app.post("/reverb/advanced/")
async def process_reverb_advanced(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    settings: str = Form(...),
) -> FileResponse:
    reverb = rvb.Reverb(**json.loads(settings))
    output_file = await rvb.apply_reverb(reverb, file)

    def remove_file(file_path: str):
        os.remove(file_path)

    background_tasks.add_task(remove_file, output_file)
    return FileResponse(
        output_file,
        headers={"Content-Disposition": f"attachment; filename={file.filename}"},
        media_type="application/octet-stream",
    )


@app.post("/reverb/")
async def process_reverb(
    file: UploadFile = File(...),
    preset: str = Form(...),
) -> FileResponse:
    now = datetime.now()
    for key, value in list(cache.items()):
        if now - datetime.fromtimestamp(os.path.getmtime(value)) > DELAY_FOR_DELETION:
            os.remove(value)
            cache.pop(key)
        else:
            break
    if preset == "auto":
        contents = await file.read()
        y = librosa.load(io.BytesIO(contents))[0]
        preset = predict(ml_param["scaler"], ml_param["model"], y)
        await file.seek(0)
    cache_key = f"{file.filename}_{preset}"
    if cache_key in cache:
        output_file = cache[cache_key]
        filename = os.path.basename(output_file)
        return FileResponse(
            output_file,
            headers={"Content-Disposition": f"attachment; filename={filename}"},
            media_type="application/octet-stream",
        )
    reverb = rvb.PresetReverb(preset)
    output_file = await rvb.apply_reverb(reverb, file)
    cache[cache_key] = output_file
    filename = os.path.basename(output_file)
    return FileResponse(
        output_file,
        headers={"Content-Disposition": f"attachment; filename={filename}"},
        media_type="application/octet-stream",
    )


def start():
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
