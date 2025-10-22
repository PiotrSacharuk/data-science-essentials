from http import HTTPStatus
from pathlib import Path
from threading import Lock

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.data.sources.pandas_source import PandasSource

app = FastAPI()
lock = Lock()


def get_pandas_source(request: "DataLoadRequest") -> PandasSource:
    """Helper to create PandasSource with project root cache dir."""
    project_root = Path(__file__).parent.parent
    cache_dir = str(project_root / "data" / "cache")
    return PandasSource(
        request.source_url,
        separator=request.separator,
        header=request.header,
        cache_dir=cache_dir,
    )


class DataLoadRequest(BaseModel):
    source_url: str
    separator: str = ","
    header: bool = True


class DataSliceRequest(DataLoadRequest):
    n: int = 5


@app.post("/data/load", tags=["Pandas"])
def load_data(request: DataLoadRequest):
    try:
        source = get_pandas_source(request)
        df = source.read_csv_file()
        return {
            "status": "success",
            "shape": df.shape,
            "columns": df.columns.tolist(),
            "preview": df.to_dict(orient="records"),
        }
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))


@app.post("/data/head", tags=["Pandas"])
def data_head(request: DataSliceRequest):
    try:
        source = get_pandas_source(request)
        result = source.head(request.n).to_dict(orient="records")
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))


@app.post("/data/tail", tags=["Pandas"])
def data_tail(request: DataSliceRequest):
    try:
        source = get_pandas_source(request)
        result = source.tail(request.n).to_dict(orient="records")
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))


@app.post("/data/describe", tags=["Pandas"])
def data_describe(request: DataLoadRequest):
    try:
        source = get_pandas_source(request)
        result = source.describe().to_dict()
        return {"status": "success", "statistics": result}
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
