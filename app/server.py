import logging
from time import perf_counter
from typing import Any

from fastapi import FastAPI, Request

from app.routes.pandas import router as pandas_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)

log = logging.getLogger(__name__)

app = FastAPI()

app.include_router(pandas_router)


@app.middleware("http")
async def timing(request: Request, call_next: Any) -> Any:
    start_time = perf_counter()
    response = await call_next(request)
    duration = perf_counter() - start_time
    log.info(
        f"[metric:call.duration] {request.method} {request.url} "
        f"{response.status_code} {duration:.2f}s"
    )
    return response


if __name__ == "__main__":
    import uvicorn

    from app.config import settings

    uvicorn.run(app, host=settings.server_host, port=settings.server_port)
