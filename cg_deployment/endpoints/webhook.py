import logging
from typing import List

from cg_deployment.config import EnvConfig
from cg_deployment.models import DeploymentPayload, StatusPayload
from cg_deployment.utils import (
    get_latest_deployments,
    set_deployment_state,
    set_deployment_url,
    update_trigger_file,
    verify_signature,
    verify_token,
)
from fastapi import FastAPI, HTTPException, Request, Response
from starlette.responses import PlainTextResponse

LOG = logging.getLogger(__name__)
app = FastAPI()
envconfig = EnvConfig()


@app.exception_handler(HTTPException)
def inform_error(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


@app.post("/deployment")
async def deployment(payload: DeploymentPayload, request: Request):
    await verify_signature(request=request)
    LOG.info(payload.dict())
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
    set_deployment_url(status_url=payload.status_url, environment_url=payload.environment_url)
    set_deployment_state(status_url=payload.status_url, state=payload.status)
    return Response(status_code=200)
