from fastapi import FastAPI
from ops.book.routes import book_router
from ops.author.routes import author_router
from db.session import engine

from models import model

model.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(book_router, prefix="/book", tags=["books"])
app.include_router(author_router, prefix="/author", tags=["authors"])
