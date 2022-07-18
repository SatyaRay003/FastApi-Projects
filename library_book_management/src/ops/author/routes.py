from fastapi import APIRouter
from fastapi import Depends
from db.session import SessionLocal
from sqlalchemy.orm import Session
from models.schemas import Response, RequestAuthor
from validations.data_validation import isnone
from ops.author import crud

author_router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@author_router.post("/create")
async def create_author(request: RequestAuthor, db: Session = Depends(get_db)):
    author_id = request.parameter.author_id
    _author = crud.get_author_by_id(db, author_id)
    if not isnone(_author):
        return Response(status="Already Exists",
                        code="409",
                        message=f"Already a record exist with author id {author_id}").dict(exclude_none=True)
    crud.create_author(db, author=request.parameter)
    return Response(status="OK",
                    code="200",
                    message="Author added sucessfully").dict(exclude_none=True)


@author_router.get("/")
async def get_authors(skip: int = 0, limit: int = 100, db:  Session = Depends(get_db)):
    _author = crud.get_author(db, skip, limit)
    if len(_author) == 0:
        return Response(status="Data Not Found",
                        code="404",
                        message="Currently No Data Available").dict(exclude_none=True)
    return Response(status="OK",
                    code="200",
                    message="Sucessfully fetch the Data",
                    result=_author)


@author_router.get("/{author_id}")
async def get_authors(author_id, db: Session = Depends(get_db)):
    _author = crud.get_author_by_id(db, author_id)
    if isnone(_author):
        return Response(status="Data Not Found",
                        code="404",
                        message="author id doesn't exist").dict(exclude_none=True)
    return Response(status="Ok",
                    code="200",
                    message="Suessfully fetch all the Data",
                    result=_author)

        
@author_router.patch("/updateDescription")
async def update_description(request: RequestAuthor, db: Session = Depends(get_db)):
    _author = crud.update_description(db, request.parameter)
    if _author.strip() == '':
        return Response(status="Data Not Found",
                        code="404",
                        message="The authod id doesn't exist").dict(exclude_none=True)
    return Response(status="OK", 
                    code="200",
                    message=_author).dict(exclude_none=True)

@author_router.delete("/delete/{author_id}")
async def delete_author(author_id, db: Session = Depends(get_db)):
    _author = crud.remove_author(db, author_id)
    if _author.strip() == '':
        return Response(status="Data Not Found",
                        code="404",
                        message="The author id doesn't exist").dict(exclude_none=True)
    return Response(status="OK",
                    code="200",
                    message=_author).dict(exclude_none=True)
