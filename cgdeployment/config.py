from typing import Optional

from pydantic import BaseSettings


class EnvConfig(BaseSettings):
    authorization_token: Optional[str]
    webhook_token: Optional[str]

    class Config:
        env_file = ".env"
