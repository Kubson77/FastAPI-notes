import models  # `models` contains ORM model classes that define the database structure
import uvicorn
from database import engine
from fastapi import FastAPI
from routers import todos

app = FastAPI()

# Create all tables defined by the ORM models in the database.
# Base.metadata contains metadata that SQLAlchemy uses to manage database tables.
# The `create_all` function looks for all classes derived from `Base` (e.g., model classes) and creates tables in the database.
# It will only create tables that do not already exist, making it safe to run on app startup.
models.Base.metadata.create_all(bind=engine)

# Import the `todos` router from the routers module and include it in the FastAPI application.
# The `include_router` method allows us to modularize our application by splitting
# different sets of routes into separate files or "routers." This keeps our main application
# file organized and manageable, especially as the number of endpoints grows.
# Here, we include the `todos` router, which defines all routes related to `to-do` tasks.
app.include_router(todos.router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=5001, reload=True)
