from typing import List
from pydantic import BaseModel, Field

from blogs.response.blog_response import BlogResponse

class UserResponse(BaseModel):
    id: int
    user_name: str=Field(..., alias='name')
    email: str
    password: str
    blogs: List[BlogResponse] = Field(..., alias='blog')
    class Config:
        orm_mode = True
