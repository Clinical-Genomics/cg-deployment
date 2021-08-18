import json

import requests
from cgdeployment.config import EnvConfig
from cgdeployment.models import PullRequestPayload, Payload, DeploymentPayload

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


def parse_pull_request_trigger(payload: PullRequestPayload) -> bool:
    if payload.action == "edited":
        original_text = payload.changes.get("body").get("from")
        modified_text = payload.pull_request.get("body")
        if (
            envconfig.deployment_diff_trigger in modified_text
            and envconfig.deployment_diff_trigger not in original_text
        ):
            print("TRIGGERED")
            return True


def create_deployment(payload: PullRequestPayload):
    ref = payload.pull_request.get("head").get("ref")
    repo = payload.pull_request.get("head").get("repo").get("name")
    organization = payload.pull_request.get("head").get("repo").get("owner").get("login")
    response = requests.post(
        url=envconfig.deployments_post_uri.format(organization=organization, repository=repo),
        data=json.dumps(
            {
                "repo": repo,
                "ref": ref,
                "environment": "stage",
            }
        ),
        headers={
            "content-type": "application/vnd.github.v3+json",
            "authorization": f"token {envconfig.authorization_token}",
        },
    )
    print(response.text)


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
