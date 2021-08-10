from typing import Optional

from fastapi import FastAPI, File, Form, HTTPException, Response, UploadFile, Request
from pydantic import NameEmail, BaseSettings, BaseModel
from starlette.responses import PlainTextResponse

app = FastAPI()


class Payload(BaseModel):
    action: Optional[str]
    issue: Optional[dict]

    class Config:
        extra = "allow"


@app.exception_handler(HTTPException)
def inform_error(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


@app.post("/payload")
async def payload(payload: Payload):
    print(payload)
    return Response(status_code=200)
