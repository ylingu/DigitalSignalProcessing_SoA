import os

import uvicorn
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from dsp import reverberation as rvb

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex="https://localhost:*",
    allow_methods=["GET", "POST"],
)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILES_DIRECTORY = os.path.join(BASE_DIR, "input_files")
PROCESSED_FILES_DIRECTORY = os.path.join(BASE_DIR, "processed_files")

os.makedirs(INPUT_FILES_DIRECTORY, exist_ok=True)
os.makedirs(PROCESSED_FILES_DIRECTORY, exist_ok=True)


@app.post("/reverb/")
async def process_reverb(preset: str, file: UploadFile = File(...)) -> dict[str, str]:
    reverb = rvb.PresetReverb(preset)
    input_file = os.path.join(INPUT_FILES_DIRECTORY, file.filename)
    output_file = os.path.join(PROCESSED_FILES_DIRECTORY, file.filename)
    with open(input_file, "wb") as f:
        f.write(file.file.read())
    reverb.apply_reverb(input_file, output_file)
    return {"processed_file_url": f"/download/{file.filename}"}


@app.get("/download/{filename}")
async def download_file(filename: str) -> FileResponse:
    file_path = os.path.join(PROCESSED_FILES_DIRECTORY, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(
        file_path, filename=filename, media_type="application/octet-stream"
    )


def start():
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
