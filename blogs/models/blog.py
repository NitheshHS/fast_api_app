from sqlalchemy import Column, Integer, String

from blogs.database.database import Base


class Blog(Base):
    __tablename__ = "Blog"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    body = Column(String)
