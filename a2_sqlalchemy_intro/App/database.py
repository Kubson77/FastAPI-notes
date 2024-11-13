from sqlalchemy import create_engine  # Creates a connection to the database
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Specify the database URL.
# Here we're using SQLite and the database file will be `todosapp.db` in the current directory.
SQLALCHEMY_DATABASE_URL = "sqlite:///./todosapp.db"

# Create a SQLAlchemy engine instance.
# The engine manages the connection to the SQLite database.
# The connect_args parameter is specific to SQLite, allowing multiple threads to access the database in this setup.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# `sessionmaker` manages sessions to interact with the database.
# `Session` class is bound to the engine, allowing sessions created from this class to interact with the database.
# `autocommit=False` Transactions will not be committed automatically. They need to be committed explicitly.
# `autoflush=False` The session won’t automatically push changes to the database until explicitly committed.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for all models in the app.
# All ORM (Object-Relational Mapping) model classes will inherit from this class.
# Base provides a foundation for mapping Python classes to database tables.
Base = declarative_base()
