from typing import Dict

import httpx
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import ExpiredSignatureError, JWTError, jwt

from ..config import settings

# Variables de entorno cargadas desde el .env
AUTH0_DOMAIN = settings.AUTH0_DOMAIN
API_AUDIENCE = settings.AUTH0_AUDIENCE
ALGORITHMS = [settings.JWT_ALGORITHM]

auth_scheme = HTTPBearer()


async def get_rsa_key(token_header: Dict) -> Dict:
    """Obtener la clave pública RSA desde Auth0 de manera asíncrona."""
    jwks_url = f"https://{AUTH0_DOMAIN}/.well-known/jwks.json"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(jwks_url)
            response.raise_for_status()

        jwks = response.json()
    except (httpx.HTTPError, ValueError) as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener las claves públicas de Auth0: {str(e)}",
        )

    for key in jwks["keys"]:
        if key["kid"] == token_header["kid"]:
            return {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"],
            }

    raise HTTPException(status_code=401, detail="No se encontró una clave válida.")


async def verify_jwt(token: str) -> Dict:
    """Verifica y decodifica el JWT."""
    try:
        token_header = jwt.get_unverified_header(token)
        rsa_key = await get_rsa_key(token_header)

        if rsa_key:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer=f"https://{AUTH0_DOMAIN}/",
            )
            return payload

    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="El token ha expirado.")
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Token inválido: {str(e)}")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error inesperado al validar el token: {str(e)}"
        )

    raise HTTPException(status_code=401, detail="No se pudo validar el token.")


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends()):
    """Extrae y verifica el usuario desde el token JWT."""
    token = credentials.credentials
    payload = await verify_jwt(token)
    return payload
