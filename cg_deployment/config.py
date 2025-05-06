import logging
from typing import Optional

from pydantic import BaseSettings, validator

logging.basicConfig(level=logging.INFO)


class EnvConfig(BaseSettings):
    authorization_token: Optional[str]
    webhook_token: Optional[str]
    triggers_dir: Optional[str]
    environments: Optional[str]

    @validator("environments")
    def return_env_list(cls, value) -> list:
        if value:
            return value.split(",")

    class Config:
        env_file = ".env"
