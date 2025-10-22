from http import HTTPStatus
from pathlib import Path
from threading import Lock

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.data.sources.pandas_source import PandasSource

app = FastAPI()
lock = Lock()


class DataLoadRequest(BaseModel):
    source_url: str
    separator: str = ","
    header: bool = True


@app.post("/data/load", tags=["Pandas"])
def load_data(request: DataLoadRequest):
    try:
        project_root = Path(__file__).parent.parent
        cache_dir = str(project_root / "data" / "cache")
        source = PandasSource(
            request.source_url,
            separator=request.separator,
            header=request.header,
            cache_dir=cache_dir,
        )
        df = source.read_csv_file()
        return {
            "status": "success",
            "shape": df.shape,
            "columns": df.columns.tolist(),
            "preview": df.head(5).to_dict(orient="records"),
        }
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))


@app.post("/data/head", tags=["Pandas"])
def data_head(request: DataLoadRequest):
    try:
        project_root = Path(__file__).parent.parent
        cache_dir = str(project_root / "data" / "cache")
        source = PandasSource(
            request.source_url,
            separator=request.separator,
            header=request.header,
            cache_dir=cache_dir,
        )
        result = source.head(5).to_dict(orient="records")
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))


@app.post("/data/tail", tags=["Pandas"])
def data_tail(request: DataLoadRequest):
    try:
        project_root = Path(__file__).parent.parent
        cache_dir = str(project_root / "data" / "cache")
        source = PandasSource(
            request.source_url,
            separator=request.separator,
            header=request.header,
            cache_dir=cache_dir,
        )
        result = source.tail(5).to_dict(orient="records")
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))


@app.post("/data/describe", tags=["Pandas"])
def data_describe(request: DataLoadRequest):
    try:
        project_root = Path(__file__).parent.parent
        cache_dir = str(project_root / "data" / "cache")
        source = PandasSource(
            request.source_url,
            separator=request.separator,
            header=request.header,
            cache_dir=cache_dir,
        )
        result = source.describe().to_dict()
        return {"status": "success", "statistics": result}
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
