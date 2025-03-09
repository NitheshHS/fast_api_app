from typing import List

from fastapi import FastAPI, Depends, HTTPException, status

from blogs.models.model import Blog
from .database.database import SessionLocal, Base, engine
from .requests.blog_request import BlogRequest
from .response.blog_response import BlogResponse


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
