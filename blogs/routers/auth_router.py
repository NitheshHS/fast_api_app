from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from jose import JWTError, jwt

from blogs.database.database import SessionLocal, get_db
from blogs.models.user import User
from blogs.util.utility import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY, authenticate_user, create_access_token, get_user, oauth2_scheme
from ..util.loggers import logger

# FastAPI router
router = APIRouter(
    tags=['Auth']
)

@router.post("/token", response_model=dict)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db:SessionLocal=Depends(get_db)):
    logger.info(f"User {form_data.username} is trying to login")
    user = authenticate_user(form_data.username, form_data.password, db)
    logger.info(f"User {form_data.username} is authenticated user: {user.email}")
    if not user:
        logger.info(f"User {form_data.username} is not authenticated")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    logger.info(f"User {form_data.username} generating access token")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

async def get_current_user(token: str = Depends(oauth2_scheme), db: SessionLocal = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        logger.info(f"Validating token {token}")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        logger.info(f"Token {token} is validated for user {email}")
        if email is None:
            logger.info(f"Token {token} is not validated for user {email}")
            raise credentials_exception
        token_data = User(email=email)
    except JWTError:
        raise credentials_exception
    user = get_user(email, db=db)
    logger.info(f"User {user} is validated for token {token}")
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    logger.info(f"Checking User {current_user} is active or Inactive")
    if current_user.email is None:
        logger.info(f"User {current_user} is inactive")
        raise HTTPException(status_code=400, detail="Inactive user")
    logger.info(f"User {current_user} is active")
    return current_user