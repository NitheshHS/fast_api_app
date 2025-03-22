from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from blogs.database.database import Base
from blogs.response.blog_response import BlogResponse


class User(Base):
    __tablename__ = "User"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True)
    password = Column(String)
    blog = relationship("Blog", back_populates="created_by", lazy='joined')