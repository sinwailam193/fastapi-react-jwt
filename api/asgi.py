import uvicorn

from app.main import create_app
from app.core.config import settings

api = create_app(settings=settings)

if __name__ == "__main__":
    uvicorn.run("asgi:api", host="localhost", port=8000, reload=True)
