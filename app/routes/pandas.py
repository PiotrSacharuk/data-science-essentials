import logging
from functools import wraps
from http import HTTPStatus
from pathlib import Path
from typing import Callable

from fastapi import APIRouter, HTTPException

from app.models.pandas import DataLoadRequest, DataSliceRequest
from src.data.sources.pandas_source import PandasSource

log = logging.getLogger(__name__)

router = APIRouter(prefix="/data", tags=["Pandas"])


def handle_pandas_exceptions(func: Callable) -> Callable:
    """Decorator to handle exceptions in pandas route functions."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))

    return wrapper


def get_pandas_source(request: DataLoadRequest) -> PandasSource:
    """Helper to create PandasSource with project root cache dir."""
    project_root = Path(__file__).parent.parent.parent
    cache_dir = str(project_root / "data" / "cache")
    source_url = request.source_url
    log.info(f"Get pandas data from {source_url}")
    return PandasSource(
        source_url,
        separator=request.separator,
        header=request.header,
        cache_dir=cache_dir,
    )


@router.post("/load")
@handle_pandas_exceptions
def load_data(request: DataLoadRequest):
    source = get_pandas_source(request)
    df = source.read_csv_file()
    return {
        "status": "success",
        "shape": df.shape,
        "columns": df.columns.tolist(),
        "preview": df.to_dict(orient="records"),
    }


@router.post("/head")
@handle_pandas_exceptions
def data_head(request: DataSliceRequest):
    source = get_pandas_source(request)
    result = source.head(request.n).to_dict(orient="records")
    log.info(f"Returning head with {request.n} records")
    return {"status": "success", "data": result}


@router.post("/tail")
@handle_pandas_exceptions
def data_tail(request: DataSliceRequest):
    source = get_pandas_source(request)
    result = source.tail(request.n).to_dict(orient="records")
    log.info(f"Returning tail with {request.n} records")
    return {"status": "success", "data": result}


@router.post("/describe")
@handle_pandas_exceptions
def data_describe(request: DataLoadRequest):
    source = get_pandas_source(request)
    result = source.describe().to_dict()
    log.info("Returning data description statistics")
    return {"status": "success", "statistics": result}
