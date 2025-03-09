from pydantic import BaseModel, Field


class BlogResponse(BaseModel):
    id: int
    title: str
    content: str=Field(..., alias='body')

    class Config:
        orm_mode = True