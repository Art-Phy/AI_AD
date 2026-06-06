
import uvicorn

def main():
    uvicorn.run(
        "aidetect.api.app:app",
        host="127.0.0.1",
        port=8000,
        reload=False,
    )
