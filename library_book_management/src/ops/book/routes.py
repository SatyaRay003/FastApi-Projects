from fastapi import APIRouter, HTTPException, Path
from fastapi import Depends
from db.session import SessionLocal
from sqlalchemy.orm import Session
from models.schemas import BookSchema, Request, Response, RequestBook
from validations.data_validation import isnone

from ops.book import crud
from ops.author import crud as author_crud

book_router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@book_router.post("/create")
async def create_book_service(request: RequestBook, db: Session = Depends(get_db)):
    book_id = request.parameter.book_id
    author_id = request.parameter.author_id
    _books = crud.get_book_by_id(db, book_id)
    _author = author_crud.get_author_by_id(db, author_id)
    if not isnone(_books):
        return Response(status="Already Exists", 
                        code="409", 
                        message=f"Already a record exist with book id {book_id}").dict(exclude_none=True)
    if isnone(_author):
        return Response(status="Data Not Found",
                        code="404",
                        message=f"The author id {author_id} doesn't exist").dict(exclude_none=True)
    crud.create_book(db, book=request.parameter)
    return Response(status="Ok",
                    code="200",
                    message="Book created successfully").dict(exclude_none=True)

@book_router.get("/")
async def get_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    _books = crud.get_book(db, skip, limit)
    if len(_books) == 0:
        return Response(status="Data Not Found", code="404", message="Currently No Data Available").dict(exclude_none=True)
    return Response(status="Ok", code="200", message="Success fetch all data", result=_books)

@book_router.get("/{book_id}")
async def get_books(book_id, db: Session = Depends(get_db)):
    _books = crud.get_book_by_id(db, book_id)
    if isnone(_books):
        return Response(status="Data Not Found", code="404", message="book id desn't exist").dict(exclude_none=True)
    return Response(status="Ok", code="200", message="Success fetch all data", result=_books)


@book_router.patch("/addCopies")
async def add_books(request: RequestBook, db: Session = Depends(get_db)):
    _book = crud.add_book(db, book_id=request.parameter.book_id,
                                 copy_count=request.parameter.copy_count)
    if _book.strip() == '':
        return Response(status="Data Not Found", code="404", message="book id desn't exist").dict(exclude_none=True)
    return Response(status="Ok", code="200", message=_book).dict(exclude_none=True)


@book_router.patch("/reductCopies")
async def reduct_books(request: RequestBook, db: Session = Depends(get_db)):
    _book = crud.reduct_book(db, book_id=request.parameter.book_id)
    if _book.strip() == '':
        return Response(status="Data Not Found", code="404", message="book id desn't exist").dict(exclude_none=True)
    return Response(status="Ok", code="200", message=_book).dict(exclude_none=True)


@book_router.delete("/delete")
async def delete_book(request: RequestBook,  db: Session = Depends(get_db)):
    _book = crud.remove_book(db, book_id=request.parameter.book_id)
    if _book.strip() == '':
        return Response(status="Data Not Found", code="404", message="book id desn't exist").dict(exclude_none=True)
    return Response(status="Ok", code="200", message=_book).dict(exclude_none=True)


