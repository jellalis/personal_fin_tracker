from pydantic_settings import BaseSettings
from pydantic import computed_field

# Settings reads environment variables automatically from the .env file
# Each field here MUST exist in .env — pydantic-settings raises a clear error if one is missing
# This gives us one central place to manage all configuration — no scattered os.getenv() calls
class Settings(BaseSettings):
    # These fields map directly to variables in .env (same name, case-insensitive)
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    SECRET_KEY: str  # used to sign and verify JWT tokens — must be long, random, and secret

    # @computed_field builds a derived field from existing ones — it is NOT read from .env
    # DATABASE_URL assembles the full connection string that SQLAlchemy's create_engine() needs
    # Format: postgresql://user:password@host:port/dbname
    @computed_field
    @property
    def DATABASE_URL(self) -> str:
         return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    # Tells pydantic-settings to look for a .env file in the project root directory
    model_config = {"env_file": ".env"}

# A single shared instance used throughout the entire application
# Always import this object, not the class: from core.config import settings
settings = Settings()
