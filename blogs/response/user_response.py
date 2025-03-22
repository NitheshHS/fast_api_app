from pydantic import BaseModel, Field

class UserResponse(BaseModel):
    id: int
    user_name: str=Field(..., alias='name')
    email: str
    password: str

    class Config:
        orm_mode = True