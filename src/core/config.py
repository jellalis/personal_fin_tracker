from pydantic_settings import BaseSettings
from pydantic import computed_field
from typing import Optional

class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    SECRET_KEY: str
    # Optional SSL mode — not set locally, set to "require" on Render/Neon
    POSTGRES_SSLMODE: Optional[str] = None

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        base_url = f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        # Append SSL mode if set — required for Neon and most cloud PostgreSQL providers
        if self.POSTGRES_SSLMODE:
            return f"{base_url}?sslmode={self.POSTGRES_SSLMODE}"
        return base_url

    model_config = {"env_file": ".env"}

settings = Settings()