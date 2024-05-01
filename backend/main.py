import json
import os
import shutil
from contextlib import asynccontextmanager
from datetime import datetime, timedelta

import uvicorn
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from dsp import reverberation as rvb

DELAY_FOR_DELETION = timedelta(hours=1)


@asynccontextmanager
async def lifespan(app: FastAPI):
    os.makedirs(rvb.PROCESSED_FILES_DIRECTORY, exist_ok=True)
    yield
    shutil.rmtree(rvb.PROCESSED_FILES_DIRECTORY, ignore_errors=True)


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
    file: UploadFile = File(...),
    settings: str = Form(...),
) -> FileResponse:
    reverb = rvb.Reverb(**json.loads(settings))
    output_file = await rvb.apply_reverb(reverb, file)
    return FileResponse(
        output_file,
        headers={"Content-Disposition": f"attachment; filename={file.filename}"},
        media_type="application/octet-stream",
    )


@app.post("/reverb/")
async def process_reverb(
    file: UploadFile = File(...), preset: str = Form(...)
) -> FileResponse:
    now = datetime.now()
    for key, value in list(cache.items()):
        if now - datetime.fromtimestamp(os.path.getmtime(value)) > DELAY_FOR_DELETION:
            os.remove(value)
            cache.pop(key)
        else:
            break
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
