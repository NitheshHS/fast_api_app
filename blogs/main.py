from typing import List

from fastapi import FastAPI, Depends, HTTPException, status

from blogs.models.blog import Blog
from blogs.requests.user_request import UserRequest
from blogs.response.user_response import UserResponse
from .database.database import SessionLocal, Base, engine
from .requests.blog_request import BlogRequest
from .response.blog_response import BlogResponse
from .models.user import User
from passlib.context import CryptContext


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post('/blog', response_model=BlogResponse, status_code=status.HTTP_201_CREATED)
def create_blog(blog_request: BlogRequest, db: SessionLocal = Depends(get_db)):
   blog = Blog(title=blog_request.title, body=blog_request.content)
   db.add(blog)
   db.commit()
   db.refresh(blog)
   return blog

@app.get('/blog', response_model=List[BlogResponse], status_code=status.HTTP_200_OK)
def get_all_blogs(db: SessionLocal = Depends(get_db)):
    blogs = db.query(Blog).all()
    return blogs

@app.get('/blog/{blog_id}', response_model=BlogResponse, status_code=status.HTTP_200_OK)
def get_blog(blog_id: int, db: SessionLocal = Depends(get_db)):
    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if blog is None:
        raise HTTPException(status_code=404, detail='Blog not found')
    else:
        return blog

@app.put('/blog/{blog_id}', response_model=BlogResponse, status_code=status.HTTP_200_OK)
def update_blog(blog_id: int, blog_request: BlogRequest, db: SessionLocal = Depends(get_db)):
    blogs = db.query(Blog).filter(Blog.id == blog_id).first()
    if blogs is None:
        raise HTTPException(status_code=404, detail='Blog does not exist')
    else:
        blogs.title = blog_request.title
        blogs.body = blog_request.body
        db.commit()
        db.refresh(blogs)
        return blogs

@app.delete('/blog', status_code=status.HTTP_204_NO_CONTENT)
def delete_all_blogs(db: SessionLocal = Depends(get_db)):
    db.query(Blog).delete()
    db.commit()
    return {'message': 'all blogs deleted'}

@app.delete('/blog/{blog_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(blog_id: int, db: SessionLocal = Depends(get_db)):
    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if blog is None:
        raise HTTPException(status_code=404, detail="Blog does not exist")
    db.delete(blog)
    db.commit()
    return {'data': 'success', 'msg': f'Blog deleted: {blog.title}'}

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.post('/user', status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user_request: UserRequest, db: SessionLocal = Depends(get_db)):
    hashed_password=password_context.hash(user_request.password)
    user = User(name=user_request.user_name, email=user_request.email, password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@app.get('/user/{user_id}', response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_user(user_id:int, db: SessionLocal = Depends(get_db)):
    user = db.query(User).filter(user_id == User.id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User does not exist")
    return user

@app.get('/user', response_model=List[UserResponse], status_code=status.HTTP_200_OK)
def get_all_users(db: SessionLocal = Depends(get_db)):
    users = db.query(User).all()
    if users is None:
        raise HTTPException(status_code=404, detail="No users found")
    return users

@app.put('/user/{user_id}', response_model=UserResponse, status_code=status.HTTP_200_OK)
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

@app.delete('/user/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id:int, db: SessionLocal = Depends(get_db)):
    user = db.query(User).filter(user_id == User.id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User does not exist")
    db.delete(user)
    db.commit()
    return {'data': 'success', 'msg': f'User deleted: {user.name}'}

