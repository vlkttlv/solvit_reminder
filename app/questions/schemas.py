from pydantic import BaseModel


class SQuestion(BaseModel):
    id: int
    url: str
    grade: str
    technology: str

    class Config:
        from_attributes = True
