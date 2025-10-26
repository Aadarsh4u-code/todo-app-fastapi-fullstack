from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
import pytest
from app.models import Users

from app.database import Base
from app.main import app
from app.models import Todos
from app.router.auth import bcrypt_context

SQLALCHEMY_DATABASE_URL_SQLITE = "sqlite:///test_todos.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL_SQLITE, poolclass=StaticPool, connect_args={"check_same_thread": False})

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {
        'username': 'aadarsh4u',
        'id': 1,
        'user_role': 'admin',
    }


client = TestClient(app)

@pytest.fixture
def test_todo():
    todo = Todos(
        title='Learn to code!',
        description='Need to learn everyday!',
        priority=5,
        complete=False,
        owner_id=1
    )
    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo

    with engine.connect() as conn:
        conn.execute(text("DELETE FROM todos"))
        conn.commit()

@pytest.fixture
def test_user():
    user = Users(
        username="aadarsh4u",
        email="derekheart020@gmail.com",
        first_name="aadarsh",
        last_name="kushwaha",
        hashed_password=bcrypt_context.hash("123456"),
        role="admin",
        phone_number="2222222222",
    )
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM users;"))
        conn.commit()
