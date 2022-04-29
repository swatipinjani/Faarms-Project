# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import uvicorn
import json
from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware, db

from schema import Book as SchemaBook
from schema import Customer as SchemaCustomer
from schema import FavoriteBooks as SchemaFavoriteBooks

from schema import Book
from schema import Customer

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
    db_customer = ModelCustomer(name=customer.name, password=customer.password, email=customer.email)
    db.session.add(db_customer)
    db.session.commit()
    return db_customer


@app.get('/customer/')
async def customer():
    customer = db.session.query(ModelCustomer).all()
    return customer

@app.post('/favorite_book/', response_model=SchemaFavoriteBooks)
async def book(favorite_book: SchemaFavoriteBooks):
    # book_id = favorite_book.favourite_books_list
    # book_list = json.dumps([book_id])
    db_favorite_book = ModelFavoriteBooks(customer_id=favorite_book.customer_id, favourite_books_list=favorite_book.favourite_books_list)
    db.session.add(db_favorite_book)
    db.session.commit()
    return db_favorite_book

# @app.get('/customers_favorite_book/')
# async def customers_favorite_book():
#     customers_favorite_book = db.session.query(ModelFavoriteBooks).all()
#     return customers_favorite_book

@app.get('/customers_favorite_book/{customerid}')
async def customers_favorite_book(customerid:int):
    favorite_data = db.session.query(ModelFavoriteBooks).where(ModelFavoriteBooks.customer_id == customerid).one()
    favorite_books_ids = eval(favorite_data.favourite_books_list)
    favorite_books_list = []
    for id in favorite_books_ids:
        book_data = db.session.query(ModelBook).where(ModelBook.id == id).one()
        favorite_books_list.append(book_data)
    return favorite_books_list


@app.get('/customers_count_favorite_book/')
async def customers_favorite_book():
    favorite_data = db.session.query(ModelFavoriteBooks).all()

    print("favorite data", favorite_data)
    # print("customer data", customer_data)
    data_dict = {}
    for each in favorite_data:
        customerid = each.customer_id
        favorite_books_ids_count = len(eval(each.favourite_books_list))
        # here query customer table where customerid match and extract customer name
        customer_data = db.session.query(ModelCustomer).where(ModelCustomer.id == customerid).one()
        customername = customer_data.name
        data_dict.update({customername: favorite_books_ids_count})

    return data_dict



# To run locally
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)





# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.
#
#
# # Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     print_hi('PyCharm')
#
# # See PyCharm help at https://www.jetbrains.com/help/pycharm/
