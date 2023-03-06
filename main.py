# main.py

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse

from time import sleep

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
    print(file)
    try:
        print(file)
        contents = file.file.read()
        with open(file.filename, "wb") as f:
            f.write(contents)

        sleep(1)

        return FileResponse(file.filename)
        # process content
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
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
