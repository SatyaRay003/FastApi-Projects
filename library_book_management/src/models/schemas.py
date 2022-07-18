from typing import Optional,List, Generic, TypeVar
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel

T = TypeVar('T')

class BookSchema(BaseModel):

    book_id: Optional[int] = None
    book_name: Optional[str] = None
    author: Optional[str] = None
    author_id: Optional[int] = None
    genre_name: Optional[str] = None
    genre_id: Optional[int] = None
    copy_count: Optional[int] = None

    class Config:
        orm_mode = True

class AuthorSchema(BaseModel):

    author_id: Optional[int] = None
    author: Optional[str] = None
    description: Optional[str] = None

    class Config:
        orm_mode = True

class RequestBook(BaseModel):
    parameter: BookSchema = Field(...)

class RequestAuthor(BaseModel):
    parameter: AuthorSchema = Field(...)

class Request(GenericModel, Generic[T]):
    parameter: Optional[T] = Field(...)

class Response(GenericModel, Generic[T]):
    code: str
    status: str
    message: str
    result: Optional[T]