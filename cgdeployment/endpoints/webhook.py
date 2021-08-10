from fastapi import FastAPI, File, Form, HTTPException, Response, UploadFile
from pydantic import NameEmail, BaseSettings
from starlette.responses import PlainTextResponse

app = FastAPI()


@app.exception_handler(HTTPException)
def inform_error(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


@app.post("/payload/")
def payload(body: str):
    print(body)
