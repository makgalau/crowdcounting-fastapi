# main.py

import os

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from supabase import create_client

import db
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
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])


@app.get("/live")
async def livecheck():
    return {"message": "Hello World"}


@app.post("/upload")
def upload(
    datetime: str = Form(...),
    gate: str = Form(...),
    file: UploadFile = File(...),
):
    try:
        contents = file.file.read()
        with open(file.filename, "wb") as f:
            f.write(contents)
            count = infer_p2pnet(file.filename)

        db.insert(supabase, datetime=datetime, gate=gate, count=count)
        return FileResponse(f"p2pnet/logs/pred{count}.jpg")
    except Exception as e:
        print(e)
        return {"message": "There was an error uploading the file"}
    finally:
        os.remove(file.filename)
        file.file.close()


@app.get("/data")
async def get_data():
    try:
        data = db.get(supabase)
        return data
    except Exception as e:
        print(e)
        return {"message": "There was an error uploading the file"}


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
