# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import uvicorn
import json
from fastapi import FastAPI, HTTPException
from fastapi_sqlalchemy import DBSessionMiddleware, db

from schema import Book as SchemaBook
from schema import Customer as SchemaCustomer
from schema import FavoriteBooks as SchemaFavoriteBooks
from models import Book as ModelBook
from models import Customer as ModelCustomer
from models import FavoriteBooks as ModelFavoriteBooks

import os
from dotenv import load_dotenv

load_dotenv('.env')

app = FastAPI()

# to avoid csrftokenError
app.add_middleware(DBSessionMiddleware, db_url=os.environ['DATABASE_URL'])


@app.get("/")
async def root():
    return {"message": "hello world"}


@app.post('/book/', response_model=SchemaBook)
async def book(book: SchemaBook):
    db_book = ModelBook(book_name=book.book_name, description=book.description, image_link=book.image_link)
    db.session.add(db_book)
    db.session.commit()
    return db_book


@app.get('/book/')
async def book():
    book = db.session.query(ModelBook).all()
    return book


@app.post('/customer/', response_model=SchemaCustomer)
async def customer(customer: SchemaCustomer):
    customer_data = db.session.query(ModelCustomer).where(ModelCustomer.email == customer.email).first()
    if customer_data:
        raise HTTPException(status_code=400, detail="Email already Exists")

    db_customer = ModelCustomer(name=customer.name, password=customer.password, email=customer.email)
    db.session.add(db_customer)
    db.session.commit()
    return db_customer

@app.get('/customer/')
async def customer():
    customer = db.session.query(ModelCustomer).all()
    return customer

@app.post('/favorite_book/{action}/{bookid}/{cutomerid}', response_model=SchemaFavoriteBooks)
async def favorite_book(action:str, bookid:str, cutomerid:int):
    book_data = db.session.query(ModelBook).where(ModelBook.id == bookid).first()
    if not book_data:
        raise HTTPException(status_code=404, detail="Given book id does not Exists")
    if action.lower() == 'like':
        try:
            data_exists = db.session.query(ModelFavoriteBooks).where(ModelFavoriteBooks.customer_id == cutomerid).first()
        except:
            data_exists = None
        if data_exists:
            try:
                favorite_books_ids = list(eval(data_exists.favourite_books_list))
            except:
                favorite_books_ids = []
            print("bookid: {}, favorite_books_ids: {}".format(bookid, favorite_books_ids))
            if int(bookid) not in favorite_books_ids:
                favorite_books_ids.append(bookid)
            setattr(data_exists, 'favourite_books_list', favorite_books_ids)
            db.session.add(data_exists)
            db.session.commit()
            db.session.refresh(data_exists)
            return data_exists
        else:
            favorite_books_ids = [bookid]
            db_favorite_book = ModelFavoriteBooks(customer_id=cutomerid, favourite_books_list=favorite_books_ids)
            db.session.add(db_favorite_book)
            db.session.commit()
            return db_favorite_book
    elif action == "dislike":
        try:
            data_exists = db.session.query(ModelFavoriteBooks).where(ModelFavoriteBooks.customer_id == cutomerid).first()
        except:
            data_exists = None
        if data_exists:
            try:
                favorite_books_ids = list(eval(data_exists.favourite_books_list))
            except:
                favorite_books_ids = []
            if int(bookid) in favorite_books_ids:
                favorite_books_ids.remove(int(bookid))
            setattr(data_exists, 'favourite_books_list', favorite_books_ids)
            db.session.add(data_exists)
            db.session.commit()
            db.session.refresh(data_exists)
            return data_exists

@app.get('/customers_favorite_book/{customerid}')
async def customers_favorite_book(customerid:int):
    favorite_data = db.session.query(ModelFavoriteBooks).where(ModelFavoriteBooks.customer_id == customerid).first()
    favorite_books_ids = eval(favorite_data.favourite_books_list)
    favorite_books_list = []
    for id in favorite_books_ids:
        book_data = db.session.query(ModelBook).where(ModelBook.id == id).first()
        favorite_books_list.append(book_data)
    return favorite_books_list


@app.get('/customers_count_favorite_book/')
async def customers_favorite_book():
    favorite_data = db.session.query(ModelFavoriteBooks).all()

    print("favorite data", favorite_data)
    data_dict = []
    for each in favorite_data:
        customerid = each.customer_id
        favorite_books_ids_count = len(eval(each.favourite_books_list))
        # here query customer table where customerid match and extract customer name
        customer_data = db.session.query(ModelCustomer).where(ModelCustomer.id == customerid).first()
        customername = customer_data.name

        data_dict.append({customername: favorite_books_ids_count, "id":customerid})
    return data_dict



# To run locally
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)

