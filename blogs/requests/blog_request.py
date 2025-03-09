from pydantic import BaseModel


class BlogRequest(BaseModel):
    title: str
    content: str