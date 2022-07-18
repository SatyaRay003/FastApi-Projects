from sqlalchemy.orm import Session
from models.model import Book
from models.schemas import BookSchema
from validations.data_validation import isnone


def get_book(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Book).offset(skip).limit(limit).all()

def get_book_by_id(db: Session, book_id: int):
    return db.query(Book).filter(Book.book_id == book_id).first()

def create_book(db: Session, book: BookSchema):
    _book = Book(book_id=book.book_id,
                book_name=book.book_name,
                author = book.author,
                author_id = book.author_id,
                genre_name = book.genre_name,
                genre_id = book.genre_id,
                copy_count = book.copy_count)
    db.add(_book)
    db.commit()
    db.refresh(_book)
    return _book

def remove_book(db: Session, book_id: int):
    _book = get_book_by_id(db=db, book_id=book_id)
    if isnone(_book):
        return ''
    db.delete(_book)
    db.commit()
    return f"Successuffly Deleted book id: {book_id}"

def add_book(db: Session, book_id: int, copy_count: int):
    _book = get_book_by_id(db=db, book_id=book_id)
    if isnone(_book):
        return ''
    previous_count = _book.copy_count 
    _book.copy_count += copy_count
    current_count = previous_count + copy_count
    db.commit()
    db.refresh(_book)
    return f"Previously there was {previous_count} copies of {_book.book_name}, Now {current_count}"

def reduct_book(db: Session, book_id: int):
    _book = get_book_by_id(db=db, book_id=book_id)
    if isnone(_book):
        return ''
    current_count = _book.copy_count 
    if current_count > 0:
        _book.copy_count -= 1
    else:
        return f"Sorry currently we have {current_count} copies, of {_book.book_name}"
    updated_count = current_count - 1
    db.commit()
    db.refresh(_book)
    return f"Previously there was {current_count} copies of {_book.book_name}, Now {updated_count}"