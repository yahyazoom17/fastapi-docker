from fastapi import FastAPI, File, UploadFile
from typing import List
from typing import Annotated
import shutil
from pathlib import Path

app = FastAPI(title="FastAPI Tutorial")

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.get("/")
def home():
    return {"message":"Welcome to FastAPI Tutorial", "description":"This is a fastapi tutorial for beginners with docker","developer":"Yahya"}

@app.post("/upload")
async def upload_file(file: Annotated[UploadFile, File(...)]):
    contents = await file.read()
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(contents)
    }

@app.post("/upload-multiple")
async def upload_multiple(
    file1: UploadFile = File(...),
    file2: UploadFile = File(...)
):
    files = [file1, file2]
    return [{"filename":f.filename, "content_type": f.content_type, "size":f.size, "metadata":{"headers":f.headers, "file":f.file}} for f in files]

@app.post("/upload-save")
async def upload_and_save(file: UploadFile = File(...)):
    dest = UPLOAD_DIR / file.filename
    with dest.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"saved_to": str(dest)}