from sqlalchemy import Column, Integer, String, Date, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
import datetime

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default='user')

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, default=datetime.date.today)
    item = Column(String, index=True)
    quantity = Column(Float, default=0)
    rate = Column(Float, default=0)
    total = Column(Float, default=0)
    patient = Column(String, nullable=True)
    department = Column(String, nullable=True)
    book_id = Column(Integer, ForeignKey('books.id'))
    entered_by = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    book = relationship('Book')
