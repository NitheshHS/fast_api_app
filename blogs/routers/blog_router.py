from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from blogs.database.database import SessionLocal
from blogs.models.blog import Blog
from blogs.models.user import User
from blogs.requests.blog_request import BlogRequest
from blogs.response.blog_response import BlogResponse
from blogs.routers.auth_router import get_current_active_user
from ..database.database import get_db
from ..util.loggers import logger


router = APIRouter(
    tags=['Blogs'],
    prefix='/blog'
)

@router.post('/', response_model=BlogResponse, status_code=status.HTTP_201_CREATED)
def create_blog(blog_request: BlogRequest, db: SessionLocal = Depends(get_db), current_user:User=Depends(get_current_active_user)):
   logger.info(f"User {current_user.email} is creating blog")
   blog = Blog(title=blog_request.title, body=blog_request.content, user_id=blog_request.user_id)
   logger.info('blog: ', blog.dict())
   db.add(blog)
   logger.info('blog added')
   db.commit()
   db.refresh(blog)
   return blog

@router.get('/', response_model=List[BlogResponse], status_code=status.HTTP_200_OK)
def get_all_blogs(db: SessionLocal = Depends(get_db),current_user:User=Depends(get_current_active_user)):
    logger.info(f"User {current_user.email} is fetching all blogs")
    blogs = db.query(Blog).all()
    return blogs

@router.get('/{blog_id}', response_model=BlogResponse, status_code=status.HTTP_200_OK)
def get_blog(blog_id: int, db: SessionLocal = Depends(get_db), current_user:User=Depends(get_current_active_user)):
    logger.info(f"User {current_user.email} is fetching blog {blog_id}")
    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if blog is None:
        logger.info(f"User {current_user.email} is fetching blog {blog_id} not found")
        raise HTTPException(status_code=404, detail='Blog not found')
    logger.info(f"User {current_user.email} is fetching blog {blog_id} found: {blog.dict()}")
    return blog

@router.put('/{blog_id}', response_model=BlogResponse, status_code=status.HTTP_200_OK)
def update_blog(blog_id: int, blog_request: BlogRequest, db: SessionLocal = Depends(get_db), current_user:User=Depends(get_current_active_user)):
    logger.info(f"User {current_user.email} is updating blog {blog_id}")
    blogs = db.query(Blog).filter(Blog.id == blog_id).first()
    if blogs is None:
        logger.info(f"User {current_user.email} is updating blog {blog_id} not found")
        raise HTTPException(status_code=404, detail='Blog does not exist')
    else:
        blogs.title = blog_request.title
        blogs.body = blog_request.content
        blogs.user_id = blog_request.user_id
        logger.info(f"User {current_user.email} is updating blog {blog_id} found: {blogs.dict()}")
        db.commit()
        db.refresh(blogs)
        return blogs

@router.delete('/', status_code=status.HTTP_204_NO_CONTENT)
def delete_all_blogs(db: SessionLocal = Depends(get_db), current_user:User=Depends(get_current_active_user)):
    logger.info(f"User {current_user.email} is deleting all blogs")
    db.query(Blog).delete()
    db.commit()
    return {'message': 'all blogs deleted'}

@router.delete('/{blog_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(blog_id: int, db: SessionLocal = Depends(get_db), current_user:User=Depends(get_current_active_user)):
    logger.info(f"User {current_user.email} is deleting blog {blog_id}")
    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if blog is None:
        logger.info(f"User {current_user.email} is deleting blog {blog_id} not found")
        raise HTTPException(status_code=404, detail="Blog does not exist")
    logger.info(f"User {current_user.email} is deleting blog {blog_id} found: {blog.dict()}")
    db.delete(blog)
    db.commit()
    return {'data': 'success', 'msg': f'Blog deleted: {blog.title}'}