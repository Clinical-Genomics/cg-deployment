import datetime
from typing import Any, List, Optional

from pydantic import BaseModel


class Payload(BaseModel):
    class Config:
        extra = "allow"


class DeploymentPayload(Payload):
    workflow_run: Optional[Any]
    workflow: Optional[Any]
    organization: Optional[dict]
    action: Optional[str]
    sender: Optional[dict]
    repository: Optional[dict]
    deployment: Optional[dict]


class StatusPayload(Payload):
    status_url: Optional[str]
    status: Optional[str]
    environment_url: Optional[str]
