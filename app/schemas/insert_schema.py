from pydantic import BaseModel

class InsertResponseSchema(BaseModel):
    msg: str
    count: int
