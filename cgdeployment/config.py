from typing import Optional

from pydantic import BaseSettings


class EnvConfig(BaseSettings):
    authorization_token: Optional[str]
    deployments_post_uri: Optional[str]
    deployment_statuses_post_uri: Optional[str]
    deployment_diff_trigger: Optional[str]

    class Config:
        env_file = ".env"
