from typing import Dict, Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.tests.utils.user import authentication_token_from_email
from app.core.config import settings
from app.api.utils import get_db
from app.db.init_db import init_db
from app.db.base_class import Base


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.drop_all(bind=engine)


def override_get_db():
    try:
        sess = TestingSessionLocal()
        init_db(sess, engine)
        yield sess
    finally:
        sess.close()


@pytest.fixture(scope="session")
def db() -> Generator:
    yield from override_get_db()


@pytest.fixture(scope="module")
def client() -> Generator:
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def user_token_headers(client: TestClient, db: Session) -> Dict[str, str]:
    return authentication_token_from_email(
        client=client, email=settings.TEST_USER, password=settings.TEST_USER_PASS, db=db
    )
