from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from ..database.database import SessionLocal, get_db
from ..models.user import User
from ..requests.user_request import UserRequest
from ..response.user_response import UserResponse
from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(
    tags=['Users'],
    prefix='/user'
)

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user_request: UserRequest, db: SessionLocal = Depends(get_db)):
    hashed_password=password_context.hash(user_request.password)
    user = User(name=user_request.user_name, email=user_request.email, password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.get('/{user_id}', response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_user(user_id:int, db: SessionLocal = Depends(get_db)):
    user = db.query(User).filter(user_id == User.id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User does not exist")
    return user

@router.get('/', response_model=List[UserResponse], status_code=status.HTTP_200_OK)
def get_all_users(db: SessionLocal = Depends(get_db)):
    users = db.query(User).all()
    if users is None:
        raise HTTPException(status_code=404, detail="No users found")
    return users

@router.put('/{user_id}', response_model=UserResponse, status_code=status.HTTP_200_OK)
def update_user(user_id:int, user_request: UserRequest, db: SessionLocal = Depends(get_db)):
    user = db.query(User).filter(user_id == User.id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User does not exist")
    user.name = user_request.user_name
    user.email = user_request.email
    user.password = user_request.password
    db.commit()
    db.refresh(user)
    return user

@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id:int, db: SessionLocal = Depends(get_db)):
    user = db.query(User).filter(user_id == User.id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User does not exist")
    db.delete(user)
    db.commit()
    return {'data': 'success', 'msg': f'User deleted: {user.name}'}