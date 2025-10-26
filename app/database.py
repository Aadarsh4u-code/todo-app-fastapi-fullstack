from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

SQLALCHEMY_DATABASE_URI_SQLite = 'sqlite:///./Todosapp.db' # For SQLite
# SQLALCHEMY_DATABASE_URI_PostgreSQL = 'postgresql://postgres:new_password@localhost:5432/todo_app_db'

# engine = create_engine(SQLALCHEMY_DATABASE_URI, connect_args={'check_same_thread': False}) # For SQLite
engine = create_engine(SQLALCHEMY_DATABASE_URI_SQLite)
SessionLocal = sessionmaker(autocommit = False, autoflush=False,  bind=engine)
Base = declarative_base()