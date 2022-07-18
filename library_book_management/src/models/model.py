from sqlalchemy import Column, Integer, String, TIMESTAMP
from db.session import Base

class Book(Base):
    __tablename__ = "books"

    book_id = Column(Integer, primary_key=True, index=True)
    book_name = Column(String)
    author = Column(String)
    author_id = Column(Integer)
    genre_name = Column(String)
    genre_id = Column(Integer)
    copy_count = Column(Integer)


class Author(Base):
    __tablename__ = "authors"

    author_id = Column(Integer, primary_key=True, index=True)
    author = Column(String)
    description = Column(String)




    
