from pydantic import BaseModel


class RecordingInfo(BaseModel):
    filename: str
    size_bytes: int
    modified_time: str
