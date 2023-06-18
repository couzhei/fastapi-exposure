from fastapi import FastAPI

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