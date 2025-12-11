from fastapi import FastAPI, HTTPException, Depends, Query
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import List, Optional


# используем SQLite 
SQLALCHEMY_DATABASE_URL = "sqlite:///./books.db"

# Создаем "движок" базы данных
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
# Создаем фабрику сессий для общения с БД
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для моделей SQLAlchemy
Base = declarative_base()

# описание таблицы "books" в базе данных
class BookDB(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    author = Column(String, nullable=False)
    year = Column(Integer, nullable=True)

# Создаем таблицы в базе данных
Base.metadata.create_all(bind=engine)

# Эти классы проверяют данные, которые приходят от пользователя и уходят к нему.

class BookBase(BaseModel):
    title: str
    author: str
    year: Optional[int] = None

class BookCreate(BookBase):
    pass

class BookResponse(BookBase):
    id: int

    class Config:
        from_attributes = True # Позволяет Pydantic читать данные из ORM-объектов

app = FastAPI(title="Simple Book Collection API")

# Dependency - нужна для получения сессии БД в каждом запросе
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Добавить новую книгу
@app.post("/books/", response_model=BookResponse)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    # Создаем объект модели SQLAlchemy из данных Pydantic
    db_book = BookDB(title=book.title, author=book.author, year=book.year)
    db.add(db_book)      # Добавляем в сессию
    db.commit()          # Сохраняем в БД
    db.refresh(db_book)  # Обновляем объект (получаем присвоенный ID)
    return db_book

# Получить все книги
@app.get("/books/", response_model=List[BookResponse])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    books = db.query(BookDB).offset(skip).limit(limit).all()
    return books

@app.get("/books/search/", response_model=List[BookResponse])
def search_books(
    title: Optional[str] = None,
    author: Optional[str] = None,
    year: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(BookDB)
    if title:
        query = query.filter(BookDB.title.contains(title))
    if author:
        query = query.filter(BookDB.author.contains(author))
    if year:
        query = query.filter(BookDB.year == year)
    
    return query.all()

# Обновить данные книги
@app.put("/books/{book_id}", response_model=BookResponse)
def update_book(book_id: int, book_update: BookCreate, db: Session = Depends(get_db)):
    db_book = db.query(BookDB).filter(BookDB.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    # Обновляем поля
    db_book.title = book_update.title
    db_book.author = book_update.author
    db_book.year = book_update.year
    
    db.commit()
    db.refresh(db_book)
    return db_book

# Удалить книгу
@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(BookDB).filter(BookDB.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    db.delete(db_book)
    db.commit()
    return {"detail": "Book deleted successfully"}