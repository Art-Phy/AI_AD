
import uvicorn

from aidetect.config import get_api_host, get_api_port


def main() -> None:
    """
    Arranca la API utilizando la configuración del entorno.
    """
    uvicorn.run(
        "aidetect.api.app:app",
        host=get_api_host(),
        port=get_api_port(),
        reload=False,
    )
