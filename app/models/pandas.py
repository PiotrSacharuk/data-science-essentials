from pydantic import BaseModel


class DataLoadRequest(BaseModel):
    source_url: str
    separator: str = ","
    header: bool = True


class DataSliceRequest(DataLoadRequest):
    n: int = 5
