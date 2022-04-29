from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base =declarative_base()

class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True, index=True)
    book_name = Column(String)
    description = Column(String)
    image_link = Column(String)


class Customer(Base):
    __tablename__ = 'customer'
    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String)
    password = Column(String)
    email = Column(String, unique=True, nullable=False)


class FavoriteBooks (Base):
    __tablename__ = 'favorite_book'
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customer.id'))
    favourite_books_list = Column(String)

