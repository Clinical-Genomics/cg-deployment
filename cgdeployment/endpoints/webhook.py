from typing import Optional

from cgdeployment.models import (
    PushPayload,
    IssuesPayload,
    IssueCommentsPayload,
    ReleasePayload,
    PullRequestPayload,
)
from fastapi import FastAPI, File, Form, HTTPException, Response, UploadFile, Request
from pydantic import NameEmail, BaseSettings, BaseModel
from starlette.responses import PlainTextResponse

app = FastAPI()


class Payload(BaseModel):
    class Config:
        extra = "allow"


@app.exception_handler(HTTPException)
def inform_error(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


@app.post("/push")
async def payload(payload: PushPayload):
    print("push post")
    print(payload)
    return Response(status_code=200)


@app.post("/issue_comment")
async def payload(payload: IssueCommentsPayload):
    print("issue comment post")
    print(payload)
    return Response(status_code=200)


@app.post("/release")
async def payload(payload: ReleasePayload):
    print("release post")
    print(payload)
    return Response(status_code=200)


@app.post("/pull_request")
async def payload(payload: PullRequestPayload):
    print("pull request post")
    print(payload)
    return Response(status_code=200)


@app.post("/issues")
async def payload(payload: IssuesPayload):
    print("issue post")
    print(payload)
    return Response(status_code=200)
