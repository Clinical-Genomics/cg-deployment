import pprint
import json
import hmac
import hashlib

import requests
from cgdeployment.config import EnvConfig
from cgdeployment.models import (
    DeploymentPayload,
)
from fastapi import FastAPI, HTTPException, Response, Request

from starlette.responses import PlainTextResponse

app = FastAPI()
envconfig = EnvConfig()

content_types = {
    "inactive": "application/vnd.github.ant-man-preview+json",
    "in_progress": "application/vnd.github.flash-preview+json",
    "queued": "application/vnd.github.flash-preview+json",
    "error": "application/vnd.github.v3+json",
    "failure": "application/vnd.github.v3+json",
    "pending": "application/vnd.github.v3+json",
    "success": "application/vnd.github.v3+json",
}


def set_deployment_state(payload: DeploymentPayload, state: str):
    deployment_url: str = f"{payload.deployment.get('url')}/statuses"
    response = requests.post(
        url=deployment_url,
        data=json.dumps(
            {
                "state": state,
            }
        ),
        headers={
            "content-type": content_types.get(state),
            "authorization": f"token {envconfig.authorization_token}",
        },
    )
    print(response.text)


async def verify_signature(
    request: Request,
):
    digester = hmac.new(key=envconfig.webhook_token.encode(), digestmod=hashlib.sha256)
    request_body = await request.body()
    digester.update(request_body)
    received_digest = request.headers.get("x-hub-signature-256")
    expected_digest = "sha256=" + digester.hexdigest()
    if not received_digest == expected_digest:
        raise HTTPException(status_code=401, detail="Invalid SHA signature")


@app.exception_handler(HTTPException)
def inform_error(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


@app.post("/deployment")
async def payload(payload: DeploymentPayload, request: Request):
    await verify_signature(request=request)
    pprint.pp(payload.dict())
    set_deployment_state(payload=payload, state="success")
    return Response(status_code=200)
