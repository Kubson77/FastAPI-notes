import uvicorn  # uvicorn is the web server used to start a FastAPI application
from fastapi import Body, FastAPI

# Initialize an instance of FastAPI, which will serve as the main application
app = FastAPI()


# Define a route for an HTTP GET request to the '/' endpoint.
@app.get("/")
async def simple_endpoint():
    # Using `async` here enables the function to handle requests concurrently,
    # which is beneficial for I/O-bound operations, such as reading from a database or making network calls.
    # However, `async` is not strictly required because FastAPI can handle this
    return {"message": "Hello World"}


"""Path Parameters"""


# Path Parameters are request parameters that have been attached to the URL
# Path Parameters are usually defined as a way to find information based on location
@app.get("/health")
async def health_endpoint():
    return {"message": "Healthy"}


# Dynamic Path Parameter: Allows the client to pass an integer parameter in the URL path
# Use `{}` to declare it in the path
@app.get("/sample/{dynamic_param}")
async def get_element(dynamic_param: int):
    return {"element": dynamic_param}


# IMPORTANT! The order of path operations matters!
# If a route with a dynamic path parameter is defined above a specific route like `/sample/1`,
# requests to `/sample/1` will match the dynamic route first (`/sample/{dynamic_param}`)
# because it appears earlier in the code. To avoid this, define more specific routes first.
@app.get("/sample/1")
async def get_first_element(dynamic_param: int):
    return {"element": dynamic_param}


"""Query Parameters"""


# Query Parameters are request parameters that have been attached after a `?`
# Query Parameters have name=value pairs
# example -> localhost:5001/sample/?query_param=12
@app.get("/sample/")
async def get_sample(query_param: int):
    # The trailing slash in `/sample/` is added for a few reasons:
    # 1. RESTful API conventions: A trailing slash often indicates a "collection" or a broader category.
    #    Here, `/sample/` could imply a list or collection of items that can be filtered by 'query_param'.
    # 2. Redirect behavior: FastAPI automatically redirects from `/sample` (no trailing slash) to `/sample/`,
    #    helping prevent 404 errors if the client omits the slash.
    # 3. Clarity for query parameters: The trailing slash before `?query_param=12` visually separates
    #    the "resource path" from the query parameters, making it clearer that this is a filter operation.
    return {"element from query": query_param}


"""POST, PUT, DELETE Methods"""


# POST request example to create a new item
@app.post("/items/")
async def create_item(item: dict = Body(...)):
    # The Body(...) function allows us to receive a JSON payload with the request
    # In a real application, this data would likely be stored in a database
    return {"message": "Item created", "item": item}


# PUT request example to update an existing item
@app.put("/items/{item_id}")
async def update_item(item_id: int, updated_item: dict = Body(...)):
    # The 'item_id' is used as a path parameter to specify which item to update
    # The updated data is provided in the request body as JSON
    return {"message": f"Item {item_id} updated", "updated_item": updated_item}


# DELETE request example to remove an item
@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    # The `item_id` is a path parameter that specifies the item to delete
    return {"message": f"Item {item_id} deleted"}


# command to run via terminal ->                                          uvicorn main:app --reload
# or (but first You have to install: pip install 'fastapi[standard]') ->  fastapi run main.py
# dev mode ->                                                             fastapi dev main.py
if __name__ == "__main__":
    # 'main:app' tells uvicorn to look for an 'app' object in this file (named 'main')
    # `host='localhost'` sets the application to run locally
    # `port=5001` sets the port number to 5001
    # `reload=True` enables automatic reloading when code changes, useful for development
    uvicorn.run("main:app", host="localhost", port=5001, reload=True)
