from  app8.settings import settings
from sqlalchemy import String, Integer, DateTime, create_engine, func, select,ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker,Session,relationship,selectinload
from datetime import datetime

engine = create_engine(settings.DATABASE_URL,pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

class Author(Base):
    __tablename__ = "author"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True,autoincrement=True)
    name: Mapped[str] = mapped_column(String(30), index=True)
    discription: Mapped[str] = mapped_column(String(100), index=True)

    books: Mapped[list["Book"]] = relationship(back_populates="author",cascade="all,delete-orphan")

class Book(Base):
    __tablename__ = "book"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True,autoincrement=True)
    title: Mapped[str] = mapped_column(String(30), index=True)
    author_id: Mapped[int] = mapped_column(Integer,ForeignKey("author.id"), index=True)
    price: Mapped[int] = mapped_column(Integer, index=True)

    author: Mapped['Author'] = relationship(back_populates="books")

    @property
    def author_name(self):
        return self.author.name if self.author else ''

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




    


    
    