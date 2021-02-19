from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.tests.utils.user import create_user_and_authenticate
from app.tests.utils.wallet import create_random_wallet


def test_create_wallet(
        client: TestClient, db: Session
) -> None:
    headers = create_user_and_authenticate(db, client)
    response = client.post(
        f"{settings.API_V1_STR}/wallet/", headers=headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["balance"] == 0
    assert "id" in content
    assert "owner_id" in content


def test_update_wallet(
        client: TestClient, db: Session, user_token_headers: dict,
) -> None:
    balance = 10
    response = client.patch(
        f"{settings.API_V1_STR}/wallet/", headers=user_token_headers, json={"balance": balance}
    )
    assert response.status_code == 200
    content = response.json()
    assert content["balance"] == balance
    assert "id" in content
    assert "owner_id" in content


def test_read_wallet(
        client: TestClient, user_token_headers: dict, db: Session
) -> None:
    owner_id = client.get(
        f"{settings.API_V1_STR}/user/whoami", headers=user_token_headers,
    ).json()['id']
    wallet = create_random_wallet(db, owner_id)
    response = client.get(
        f"{settings.API_V1_STR}/wallet", headers=user_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["balance"] == wallet.balance
    assert content["owner_id"] == wallet.owner_id
    assert content["id"] == wallet.id
