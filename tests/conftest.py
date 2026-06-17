from fastapi.testclient import TestClient
from app.main import app

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
#from alembic import command
from app.config import settings
from app.database import get_db, Base
from app.oauth2 import create_access_token
from app import models

import pytest

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.db_username}:{settings.db_password}@{settings.db_hostname}:{settings.db_port}/{settings.db_name}-test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    # command.upgrade("head")
    # command.downgrade("base")
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def overrid_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
    app.dependency_overrides[get_db] = overrid_get_db
    yield TestClient(app)

@pytest.fixture
def dummy_users(client):
    user_data = {
                "email": "user6@example.com",
                "name": "User6",
                "password": "password123"
            }
    res = client.post("/users/", json = user_data)
    assert res.status_code == 201
    user_data2 = {
                "email": "user7@example.com",
                "name": "User7",
                "password": "password123"
            }
    res2 = client.post("/users/", json = user_data2)
    assert res2.status_code == 201
    return [{**user_data, "id": res.json()["id"]},
            {**user_data2, "id": res2.json()["id"]}]

@pytest.fixture
def dummy_token(dummy_users):
    return create_access_token({"user_id": dummy_users[0]["id"]})

@pytest.fixture
def authorized_client(client, dummy_token):
    client.headers = {
        **client.headers,
        "Authorization" : f"Bearer {dummy_token}"
    }
    return client

@pytest.fixture
def dummy_posts(dummy_users, session):
    posts_data = [{
        "title": "First Post",
        "content": "First Content",
        "owner_id": dummy_users[0]["id"]
    },
    {
        "title": "Second Post",
        "content": "Second Content",
        "owner_id": dummy_users[0]["id"]
    },
    {
        "title": "Third Post",
        "content": "Third Content",
        "owner_id": dummy_users[1]["id"]
    },
    ]
    
    posts = list(map(lambda post: models.Post(**post), posts_data))

    session.add_all(posts)
    session.commit()
    posts_db = session.query(models.Post).all()
    return posts_db

@pytest.fixture
def dummy_vote(session, dummy_posts, dummy_users):
    vote = {
        "id_post": dummy_posts[0].id,
        "id_user": dummy_users[0]["id"]
    }
    new_vote = models.Vote(**vote)
    session.add(new_vote)
    session.commit()
    return vote


