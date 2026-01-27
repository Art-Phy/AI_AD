
from fastapi import HTTPException, Request

from aidetect.config import AUTH_DISABLED,  get_api_keys, is_ui_mode



API_KEY_HEADER = "X-API-Key"
API_KEY_QUERY_PARAM = "api_key"



def require_api_key(request: Request) -> str:
    """
    Valida la API key y devuelve la key usada.
    Lanza HTTPException si no es válida.

    Por defecto busca en header X-API-Key
    Si UI_MODE=1, también acepta ?api_key=... (útil para UI local)
    """
    if AUTH_DISABLED:
        return "auth_disabled"
    
    valid_keys = get_api_keys()

    if not valid_keys:
        raise HTTPException(status_code=503, detail="Auth not configured")
    
    api_key = request.headers.get(API_KEY_HEADER)

    if is_ui_mode() and not api_key:
        api_key = request.query_params.get(API_KEY_QUERY_PARAM)

    if not api_key or api_key not in valid_keys:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    return api_key
