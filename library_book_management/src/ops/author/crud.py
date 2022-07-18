from sqlalchemy.orm import Session
from models.model import Author
from models.schemas import AuthorSchema
from validations.data_validation import isnone


def get_author(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Author).offset(skip).limit(limit).all()

def get_author_by_id(db: Session, author_id: int):
    return db.query(Author).filter(Author.author_id == author_id).first()

def create_author(db:Session, author: AuthorSchema):
    _author = Author(author_id = author.author_id,
                   author = author.author,
                   description = author.description)
    db.add(_author)
    db.commit()
    db.refresh(_author)
    return _author

def update_description(db: Session, author: AuthorSchema):
    _author = get_author_by_id(db, author.author_id)
    if isnone(_author):
        return ''
    _author.description = author.description
    db.commit()
    db.refresh(_author)
    return f'Sucessfully Updated the description of {_author.author}'

def remove_author(db: Session, author_id: int):
    _author = get_author_by_id(db, author_id)
    if isnone(_author):
        return ''
    db.delete(_author)
    db.commit()
    return f'Successfully Deleted the record of {_author.author}'