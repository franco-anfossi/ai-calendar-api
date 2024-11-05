from typing import Optional

from dotenv import load_dotenv
from pydantic import ConfigDict
from pydantic_settings import BaseSettings

load_dotenv(override=True)


class Settings(BaseSettings):
    """
    Configuración de la aplicación utilizando Pydantic
    para validar y cargar variables de entorno.
    """

    # Configuración general de entorno
    ENV: str
    DEBUG: bool

    # Configuración de la base de datos
    DATABASE_URL: str

    # Configuración de Auth0
    AUTH0_DOMAIN: str
    AUTH0_AUDIENCE: Optional[str]

    # Configuración de JWT
    JWT_ALGORITHM: str = "RS256"

    # Configuración de CORS
    ALLOWED_ORIGINS: str = [
        "*",
    ]
    ALLOWED_METHODS: str = [
        "*",
    ]
    ALLOWED_HEADERS: str = [
        "*",
    ]
    ALLOW_CREDENTIALS: bool = True

    model_config = ConfigDict(case_sensitive=True)


settings = Settings()
