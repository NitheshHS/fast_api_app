from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from blogs.routers.auth_router import get_current_active_user
from ..database.database import SessionLocal, get_db
from ..models.user import User
from ..requests.user_request import UserRequest
from ..response.user_response import UserResponse
from passlib.context import CryptContext
from ..util.utility import get_password_hash
from ..util.loggers import logger

router = APIRouter(
    tags=['Users'],
    prefix='/user'
)

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user_request: UserRequest, db: SessionLocal = Depends(get_db)):
    logger.info(f"Creating user {user_request.user_name}")
    user = User(name=user_request.user_name, email=user_request.email, password=get_password_hash(user_request.password))
    logger.info(f"User {user.dict()} created")
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.get('/{user_id}', response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_user(user_id:int, db: SessionLocal = Depends(get_db), current_user:User=Depends(get_current_active_user)):
    logger.info(f"Fetching user {user_id}")
    user = db.query(User).filter(user_id == User.id).first()
    if user is None:
        logger.info(f"User {user_id} not found")
        raise HTTPException(status_code=404, detail="User does not exist")
    logger.info(f"User {user_id} found: {user.dict()}")
    return user

@router.get('/', response_model=List[UserResponse], status_code=status.HTTP_200_OK)
def get_all_users(db: SessionLocal = Depends(get_db), current_user:User=Depends(get_current_active_user)):
    logger.info(f"Fetching all users")
    users = db.query(User).all()
    if users is None:
        logger.info(f"No users found")
        raise HTTPException(status_code=404, detail="No users found")
    logger.info(f"Users found: {users.dict()}")
    return users

@router.put('/{user_id}', response_model=UserResponse, status_code=status.HTTP_200_OK)
def update_user(user_id:int, user_request: UserRequest, db: SessionLocal = Depends(get_db), current_user:User=Depends(get_current_active_user)):
    logger.info(f"Updating user {user_id}")
    user = db.query(User).filter(user_id == User.id).first()
    if user is None:
        logger.info(f"User {user_id} not found")
        raise HTTPException(status_code=404, detail="User does not exist")
    user.name = user_request.user_name
    user.email = user_request.email
    user.password = user_request.password
    logger.info(f"User {user_id} updated: {user.dict()}")
    db.commit()
    db.refresh(user)
    return user

@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id:int, db: SessionLocal = Depends(get_db), current_user:User=Depends(get_current_active_user)):
    logger.info(f"Deleting user {user_id}")
    user = db.query(User).filter(user_id == User.id).first()
    if user is None:
        logger.info(f"User {user_id} not found")
        raise HTTPException(status_code=404, detail="User does not exist")
    logger.info(f"User {user_id} deleted: {user.dict()}")
    db.delete(user)
    db.commit()
    return {'data': 'success', 'msg': f'User deleted: {user.name}'}