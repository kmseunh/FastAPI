import os

from fastapi import FastAPI, File, UploadFile

app = FastAPI()


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)) -> str:
    upload_dir = "./uploads"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    file_path = os.path.join(upload_dir, file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    return {"filename": file.filename, "path": file_path}
