from fastapi import Security, HTTPException, status
from fastapi.security.api_key import APIKeyHeader
from app.config import config

api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)

def get_api_key(api_key: str = Security(api_key_header)) -> str:
    """
    Dependency to validate the API key header.
    Returns 401 if invalid or missing.
    """
    if api_key and api_key == config.API_SECRET_KEY:
        return api_key
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API key"
    )
