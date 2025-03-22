from pydantic import BaseModel

class UserRequest(BaseModel):
    user_name: str
    email: str
    password: str