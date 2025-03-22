
from fastapi import FastAPI
from blogs.routers import auth_router, blog_router, user_router
from .database.database import Base, engine


Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth_router.router)
app.include_router(blog_router.router)
app.include_router(user_router.router)



