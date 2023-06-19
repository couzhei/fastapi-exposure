from fastapi import FastAPI

from fastapi import Path
from enum import Enum

from pydantic import BaseModel, Field

class AccountType(str, Enum):
    FREE = 'free'
    PRO = 'pro'

app = FastAPI()


@app.get("/") # i.e. in the root path when a GET request is received
async def root():
    return {"message": "Hello FastAPI "}

@app.post("/")
async def post_root():
    return {"message": "Post request success"}

# uvicorn sth:app --reload 
# you will be using quite a lot when developing with FastAPI 
# Uvicorn is our ASGI-compatible web server, and we call it directly by passing it the combination
# of the executable Python file (without the extension!) and the instantiated app (the FastAPI
# instance), separated by a colon (:). The --reload flag tells Uvicorn to reload the server
# each time we save our code, similar to Nodemon if you have worked with Node.js. You can
# run all the examples in this book that contain FastAPI apps by using this syntax, except where
# something else is suggested.


# This is our first endpoint with a dynamic path
@app.get("/car/{id}") # funny thing is that whenever I change this into an f string, it'll not work
async def root_car(id):
    return {"car_id":id}

@app.get("/carh/{id}")
async def hinted_car_id(id: int): # This time using type-hinting
    return {"car_id": id}

# it is important to remember that, like in other web frameworks, order matters.
# @app.get("/user/{id}")
# async def user(id:int):
#     return {"user": id}

# @app.get('/user/me')
# async def user():
#     return {"This is": "me"}

# writing in the above order raise an Error: Unprocessable Entity
# the proper ordering must be:
@app.get('/user/me')
async def user():
    return {"This is": "me"}

@app.get("/user/{id}")
async def user(id:int):
    return {"user": id}


@app.get("/account/{acc_type}/{months}")
async def account( acc_type:AccountType, months:int = Path(...,\
                                                           ge=3,le=12)):
    return {
        "message":"Account created",
        "account_type":acc_type,
        "months":months
        }

# Question mark in the previous expression is a separator that tells us where the query string begins,
# while the ampersands, &, allow us to add more than one assignment (the equals signs, =).
# Query parameters are usually used to apply filters, sort, order, or limit query sets, apply paginations to
# a long list of results, and similar tasks. FastAPI treats them similarly to path parameters. They will be,
# so to say, automatically picked up by FastAPI and available for processing in our endpoint functions.


# @app.get("/cars/price")
# async def cars_by_price(min_price: int=0, max_price: int=100000):
#     """ Of course, this particular solution is not very good - we do not ensure the basic condition that the
#         minimum price should be lower than the maximum price, but that can easily be handled by Pydantic
#         object-level validation.
#     """
#     return{"Message":f"Listing cars with prices between {min_price} and {max_price}"}



class CarPrice(BaseModel):
    min_price: int = Field(..., title="Minimum Price", description="The minimum price of the car")
    max_price: int = Field(..., title="Maximum Price", description="The maximum price of the car")

@app.get("/cars/price")
async def cars_by_price(min_price: int=0, max_price: int=100000):
    car_price = CarPrice(min_price=0, max_price=100000)
    if car_price.min_price >= car_price.max_price:
        raise ValueError("Invalid price range: min_price should be lower than max_price")
    return {"Message": f"Listing cars with prices between {car_price.min_price} and {car_price.max_price}"}

