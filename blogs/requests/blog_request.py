from pydantic import BaseModel, Field


class BlogRequest(BaseModel):
    title: str
    content: str
    user_id: int=Field(..., alias='user_id')