# main.py

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse, HTMLResponse

app = FastAPI()


@app.get("/live")
async def livecheck():
    return {"message": "Hello World"}


@app.post("/upload")
def upload(file: UploadFile = File(...)):
    try:
        contents = file.file.read()
        with open(file.filename, "wb") as f:
            f.write(contents)

        return FileResponse(file.filename)
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
