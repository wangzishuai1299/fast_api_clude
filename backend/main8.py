from typing import Annotated,Optional
from datetime import datetime
from fastapi import Depends, FastAPI, Query, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker,Session,selectinload
from sqlalchemy import String, Integer, DateTime, create_engine, func, select
from app8.database import get_db, Author,Book
from app8.settings import settings
from fastapi.responses import JSONResponse

def pagination(
    page:int=1,
    page_size:int=10
):
    return{
        'page':page,
        'page_size':page_size
    }

class AuthorCreate(BaseModel):
    name:str | None=None
    discription:str | None=None

class BookCreate(BaseModel):
    title:str | None=None
    author_id:int | None=None
    price:int | None=None

class BookOut(BaseModel):
    id:int
    title:str
    price:int
    author_name:str
    model_config=ConfigDict(from_attributes=True)

class BookPage(BaseModel):
    page:int
    page_size:int
    total:int
    items: list[BookOut]

app = FastAPI()

@app.exception_handler(HTTPException)
async def custom_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={'code': exc.status_code,"message": exc.detail,'data':None}
    )

@app.post("/authors",status_code=201)
def create_author(author:AuthorCreate,db=Depends(get_db)):
    db_author=Author(**author.dict())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

@app.post('/books',status_code=201)
def create_book(book:BookCreate,db=Depends(get_db)):
    db_book=Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@app.get('/books')
def get_books(
    db=Depends(get_db),
    page_info=Depends(pagination),
    keywords: Annotated[str| None,'']=None
):
    page=page_info['page']
    page_size=page_info['page_size']
    stmt_count=select(Book)
    if keywords:
        stmt_count=stmt_count.where(Book.title.contains(keywords))
    total=db.scalar(select(func.count()).select_from(stmt_count.subquery()))
    stmt=select(Book).options(selectinload(Book.author))
    if keywords:
        stmt=stmt.where(Book.title.contains(keywords))
    offset=(page-1)*page_size
    stmt=stmt.limit(page_size).offset(offset)
    items=db.scalars(stmt).all()
    return BookPage(page=page,page_size=page_size,total=total,items=items)

@app.put('/books/{book_id}')
def update_book(book_id:int,book:BookCreate,db=Depends(get_db)):
    db_book=db.get(Book,book_id)
    if db_book is None:
        raise HTTPException(status_code=404,detail='Book not found')
    for key,value in book.dict(exclude_unset=True).items():
        setattr(db_book,key,value)
    db.commit()
    db.refresh(db_book)
    return db_book

@app.delete('/books/{book_id}',status_code=204)
def delete_book(book_id:int,db=Depends(get_db)):
    db_book=db.get(Book,book_id)
    if db_book is None:
        raise HTTPException(status_code=404,detail='Book not found')
    db.delete(db_book)
    db.commit()
    return {'message':'Book deleted'}

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

if __name__=='__main__':
    import uvicorn
    uvicorn.run('main8:app',host='127.0.0.1',port=8000,reload=True)
    