from fastapi.testclient import TestClient

from app.core.config import settings


def test_get_access_token(client: TestClient) -> None:
    login_data = {
        "username": settings.TEST_USER,
        "password": settings.TEST_USER_PASS,
    }
    r = client.post(f"{settings.API_V1_STR}/login", data=login_data)
    tokens = r.json()
    assert r.status_code == 200
    assert "access_token" in tokens
    assert tokens["access_token"]
