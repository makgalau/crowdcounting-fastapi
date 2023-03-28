# main.py

from typing import Union
import os

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from p2pnet.infer import infer_p2pnet

app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/live")
async def livecheck():
    return {"message": "Hello World"}


@app.post("/upload")
def upload(file: UploadFile = File(...)):
    try:
        contents = file.file.read()
        with open(file.filename, "wb") as f:
            f.write(contents)
            count = infer_p2pnet(file.filename)
        return FileResponse(file.filename), {"message": "success", "count": count}
    except Exception as e:
        print(e)
        return {"message": "There was an error uploading the file"}
    finally:
        os.remove(file.filename)
        os.remove(f"p2pnet/logs/pred{count}.jpg")
        file.file.close()


@app.get("/")
async def main():
    content = """
        <body>
            <form action="/upload" enctype="multipart/form-data" method="post">
            <input name="file" type="file" multiple>
            <input type="submit">
            </form>
        </body>
    """
    return HTMLResponse(content=content)
