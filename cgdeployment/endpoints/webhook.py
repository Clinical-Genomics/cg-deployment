import pprint

from cgdeployment.config import EnvConfig
from cgdeployment.models import (
    Payload,
    PushPayload,
    IssuesPayload,
    IssueCommentsPayload,
    ReleasePayload,
    PullRequestPayload,
    DeploymentPayload,
)
from cgdeployment.utils import parse_pull_request_trigger, create_deployment, set_deployment_state
from fastapi import FastAPI, File, Form, HTTPException, Response, UploadFile, Request
from pydantic import NameEmail, BaseSettings, BaseModel
from starlette.responses import PlainTextResponse

app = FastAPI()
envconfig = EnvConfig()


@app.exception_handler(HTTPException)
def inform_error(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


@app.post("/push")
async def payload(payload: PushPayload):
    print("push post")
    pprint.pp(payload.dict())
    return Response(status_code=200)


@app.post("/issue_comment")
async def payload(payload: IssueCommentsPayload):
    print("issue comment post")
    pprint.pp(payload.dict())

    return Response(status_code=200)


@app.post("/release")
async def payload(payload: ReleasePayload):
    print("release post")
    pprint.pp(payload.dict())
    return Response(status_code=200)


@app.post("/pull_request")
async def payload(payload: PullRequestPayload):
    if parse_pull_request_trigger(payload=payload):
        create_deployment(payload=payload)

    print("pull request post")
    pprint.pp(payload.dict())
    return Response(status_code=200)


@app.post("/issues")
async def payload(payload: IssuesPayload):
    print("issue post")
    pprint.pp(payload.dict())
    return Response(status_code=200)


@app.post("/deployment")
async def payload(payload: DeploymentPayload):
    print("deployment post")
    pprint.pp(payload.dict())
    set_deployment_state(payload=payload, state="success")
    return Response(status_code=200)
