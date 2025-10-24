from fastapi import FastAPI

from app.routes.pandas import router as pandas_router

app = FastAPI()

app.include_router(pandas_router)

if __name__ == "__main__":
    import uvicorn

    from app.config import settings

    uvicorn.run(app, host=settings.server_host, port=settings.server_port)
