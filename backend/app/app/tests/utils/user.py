from typing import Dict

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.common.user import model, crud, schema
from app.tests.utils.utils import random_email, random_lower_string


def user_authentication_headers(
    client: TestClient, email: str, password: str
) -> Dict[str, str]:
    data = {"username": email, "password": password}

    r = client.post(f"{settings.API_V1_STR}/login", data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


def create_random_user(db: Session, password: str = None) -> model.User:
    email = random_email()
    password = password or random_lower_string()
    user_in = schema.UserCreate(username=email, email=email, password=password)
    user = crud.user.create(db=db, obj_in=user_in)
    return user


def authentication_token_from_email(
    client: TestClient, email: str, password: str, db: Session
) -> Dict[str, str]:
    """
    Return a valid token for the user with given email.

    If the user doesn't exist it is created first.
    """
    user = crud.user.get_by_email(db, email=email)
    if not user:
        user_in = schema.UserCreate(email=email, password=password)
        crud.user.create(db, user_in)

    return user_authentication_headers(client=client, email=email, password=password)


def create_user_and_authenticate(db: Session, client: TestClient):
    password = random_lower_string()
    user = create_random_user(db, password)
    headers = authentication_token_from_email(client, user.email, password, db)
    return headers
