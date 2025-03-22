from typing import Optional
from pydantic import BaseModel, Field

class BlogUserResponse(BaseModel):
    user_name: str=Field(..., alias='name')
    email: str
    class Config:
        orm_mode = True

class BlogResponse(BaseModel):
    id: int
    title: str
    content: str=Field(..., alias='body')
    created_by: Optional[BlogUserResponse] = Field(..., alias='created_by')

    class Config:
        orm_mode = True

