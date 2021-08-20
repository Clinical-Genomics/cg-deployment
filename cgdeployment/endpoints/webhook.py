import pprint
import json
import hmac
import hashlib
import time
from pathlib import Path
from typing import List

import requests
from cgdeployment.config import EnvConfig
from cgdeployment.models import (
    DeploymentPayload,
    StatusPayload,
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
    "abandoned": "application/vnd.github.v3+json",
}


def set_deployment_state(status_url: str, state: str):

    response = requests.post(
        url=status_url,
        data=json.dumps(
            {
                "state": state,
            }
        ),
        headers={
            "accept": content_types.get(state),
            "authorization": f"token {envconfig.authorization_token}",
        },
    )
    pprint.pp(json.loads(response.text))


def get_latest_deployments(payload: DeploymentPayload) -> List[DeploymentPayload]:
    environment: str = payload.deployment.get("environment")
    deployments_url: str = payload.repository.get("deployments_url")
    response = requests.get(
        url=deployments_url,
        params={"environment": environment, "per_page": 5},
        headers={
            "authorization": f"token {envconfig.authorization_token}",
        },
    )
    return [DeploymentPayload(deployment=deployment) for deployment in json.loads(response.text)]


async def verify_signature(
    request: Request,
):
    digester = hmac.new(key=envconfig.webhook_token.encode(), digestmod=hashlib.sha256)
    request_body = await request.body()
    digester.update(request_body)
    received_digest = request.headers.get("x-hub-signature-256")
    expected_digest = "sha256=" + digester.hexdigest()
    if received_digest != expected_digest:
        raise HTTPException(status_code=401, detail="Invalid SHA signature")


async def verify_token(
    request: Request,
):
    expected_token = "token " + envconfig.authorization_token
    received_token = request.headers.get("Authorization")
    if expected_token != received_token:
        raise HTTPException(status_code=401, detail="Invalid token signature")


config_template = """ENVIRONMENT={environment}
CONTAINER={container}
TAG={tag}
DEPLOYMENT_ID={deployment_id}
STATUS_URL={status_url}
TOKEN={token}
"""


async def update_trigger_file(payload: DeploymentPayload):
    environment = payload.deployment.get("environment")
    containers = payload.deployment.get("description").split(",")
    tag = payload.deployment.get("ref")
    deployment_id = payload.deployment.get("id")
    status_url = payload.deployment.get("statuses_url")
    trigger_path = Path(envconfig.triggers_dir, "deploy").with_suffix(".conf")
    for container in containers:
        with open(trigger_path, "w") as deploy_config:
            deploy_config.write(
                config_template.format(
                    environment=environment,
                    container=container,
                    tag=tag,
                    deployment_id=deployment_id,
                    status_url=status_url,
                    token=envconfig.authorization_token,
                )
            )
        time.sleep(60)


@app.exception_handler(HTTPException)
def inform_error(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


@app.post("/deployment")
async def deployment(payload: DeploymentPayload, request: Request):
    await verify_signature(request=request)
    pprint.pp(payload.dict())
    if payload.deployment.get("environment") not in envconfig.environments:
        return Response(status_code=200)
    deployments: List[DeploymentPayload] = get_latest_deployments(payload=payload)
    for deployment in deployments:
        set_deployment_state(status_url=deployment.deployment.get("statuses_url"), state="inactive")
    set_deployment_state(status_url=payload.deployment.get("statuses_url"), state="in_progress")
    await update_trigger_file(payload=payload)
    return Response(status_code=200)


@app.post("/status")
async def status(payload: StatusPayload, request: Request):
    await verify_token(request=request)
    set_deployment_state(status_url=payload.status_url, state=payload.status)
    return Response(status_code=200)
