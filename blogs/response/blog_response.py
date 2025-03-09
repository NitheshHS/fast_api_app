from pydantic import BaseModel


class BlogResponse(BaseModel):
    id: int
    title: str
    body: str

    class Config:
        orm_mode = True