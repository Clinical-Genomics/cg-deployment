import datetime
from typing import Optional, List, Any

from pydantic import BaseModel


class Payload(BaseModel):
    class Config:
        extra = "allow"


class DeploymentPayload(Payload):
    workflow_run: Optional[str]
    workflow: Optional[str]
    organization: Optional[dict]
    action: Optional[str]
    sender: Optional[dict]
    repository: Optional[dict]
    deployment: Optional[dict]
