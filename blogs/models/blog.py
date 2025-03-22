from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from blogs.database.database import Base


class Blog(Base):
    __tablename__ = "Blog"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    body = Column(String)
    user_id = Column(Integer, ForeignKey('User.id'))
    created_by = relationship("User", back_populates="blog")
