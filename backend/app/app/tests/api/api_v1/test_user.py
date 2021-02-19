from typing import Dict

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.core.config import settings
from app.common.user import crud, schema
from app.tests.utils.utils import random_email, random_lower_string


def test_whoami(
        client: TestClient, user_token_headers: Dict[str, str]
) -> None:
    r = client.get(f"{settings.API_V1_STR}/user/whoami", headers=user_token_headers)
    current_user = r.json()
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["is_superuser"] is True
    assert current_user["email"] == settings.TEST_USER


def test_create_user(
        client: TestClient, user_token_headers: dict, db: Session
) -> None:
    username = random_email()
    password = random_lower_string()
    data = {"email": username, "password": password}
    r = client.post(
        f"{settings.API_V1_STR}/user/", headers=user_token_headers, json=data,
    )
    assert 200 <= r.status_code < 300
    created_user = r.json()
    user = crud.user.get_by_email(db, email=username)
    assert user
    assert user.email == created_user["email"]


def test_create_user_existing_username(
        client: TestClient, user_token_headers: dict, db: Session
) -> None:
    username = random_email()
    password = random_lower_string()
    user_in = schema.UserCreate(email=username, password=password)
    crud.user.create(db, obj_in=user_in)
    data = {"email": username, "password": password}
    r = client.post(
        f"{settings.API_V1_STR}/user/", headers=user_token_headers, json=data,
    )
    assert r.status_code == 400
