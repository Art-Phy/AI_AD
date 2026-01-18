
from fastapi import HTTPException, Request

from aidetect.config import AUTH_DISABLED, get_api_keys



API_KEY_HEADER = "X-API-Key"



def require_api_key(request: Request) -> str:
    """
    Valida la API key y devuelve la key usada.
    Lanza HTTPException si no es válida.
    """
    if AUTH_DISABLED:
        return "auth_disabled"
    
    valid_keys = get_api_keys()
    if not valid_keys:
        raise HTTPException(status_code=503, detail="Auth not configured")
    
    api_key = request.headers.get(API_KEY_HEADER)
    if not api_key or api_key not in valid_keys:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    return api_key
