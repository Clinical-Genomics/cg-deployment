import hashlib
import hmac
import json
import logging
from pathlib import Path
from typing import List

import requests
from cg_deployment.config import EnvConfig
from cg_deployment.models import DeploymentPayload
from fastapi import HTTPException, Request

LOG = logging.getLogger(__name__)
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

config_template = """ENVIRONMENT={environment}
CONTAINER={container}
TAG={tag}
DEPLOYMENT_ID={deployment_id}
STATUS_URL={status_url}
TOKEN={token}
"""


def set_deployment_state(status_url: str, state: str) -> None:

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
    LOG.info(json.loads(response.text))


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
) -> None:
    digester = hmac.new(key=envconfig.webhook_token.encode(), digestmod=hashlib.sha256)
    request_body = await request.body()
    digester.update(request_body)
    received_digest = request.headers.get("x-hub-signature-256")
    expected_digest = "sha256=" + digester.hexdigest()
    if received_digest != expected_digest:
        raise HTTPException(status_code=401, detail="Invalid SHA signature")


async def verify_token(
    request: Request,
) -> None:
    expected_token = "token " + envconfig.authorization_token
    received_token = request.headers.get("Authorization")
    if expected_token != received_token:
        raise HTTPException(status_code=401, detail="Invalid token signature")


async def update_trigger_file(payload: DeploymentPayload) -> None:
    environment = payload.deployment.get("environment")
    container = payload.deployment.get("description")
    tag = payload.deployment.get("ref", "latest").replace("/", "-")
    deployment_id = payload.deployment.get("id")
    status_url = payload.deployment.get("statuses_url")
    trigger_path = Path(envconfig.triggers_dir, container).with_suffix(".conf")

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
    LOG.info("Trigger file updated")
