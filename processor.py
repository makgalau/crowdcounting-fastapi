from time import sleep
from fastapi.responses import FileResponse

def process(file_img):
    contents = file_img.file.read()

    with open(file_img.filename, "wb") as f:
        f.write(contents)

    sleep(1)

    return FileResponse(file_img.filename)