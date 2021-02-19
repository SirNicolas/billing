from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.tests.utils.wallet import create_random_wallet, create_transactions


def test_read_transactions(
        client: TestClient, user_token_headers: dict, db: Session
) -> None:
    owner_id = client.get(
        f"{settings.API_V1_STR}/user/whoami", headers=user_token_headers,
    ).json()['id']
    transactions = create_transactions(db, owner_id)

    response = client.get(
        f"{settings.API_V1_STR}/transaction", headers=user_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert len(content) == len(transactions)
    for response, transaction in zip(sorted(content, key=lambda x: x['id']), transactions):
        assert response["id"] == transaction.id
        assert response["amount"] == transaction.amount
        assert response["from_wallet_id"] == transaction.from_wallet_id
        assert response["to_wallet_id"] == transaction.to_wallet_id


def test_failed_transaction_creation(
        client: TestClient, db: Session, user_token_headers: dict,
) -> None:
    # Transaction amount greater than wallet balance
    owner_id = client.get(
        f"{settings.API_V1_STR}/user/whoami", headers=user_token_headers,
    ).json()['id']
    from_wallet = create_random_wallet(db, owner_id=owner_id)
    to_wallet = create_random_wallet(db, balance=100)

    body = {"amount": 100, "from_wallet_id": from_wallet.id, "to_wallet_id": to_wallet.id}
    response = client.post(
        f"{settings.API_V1_STR}/transaction/", headers=user_token_headers, json=body
    )
    assert response.status_code == 400
    error = response.json()['detail']
    assert error == "Amount of money you want to send is greater than your wallet's balance"

    # Transaction from_wallet doesn't belong to user
    body = {"amount": 100, "from_wallet_id": to_wallet.id, "to_wallet_id": from_wallet.id}
    response = client.post(
        f"{settings.API_V1_STR}/transaction/", headers=user_token_headers, json=body
    )
    assert response.status_code == 400
    error = response.json()['detail']
    assert error == f"Wallet with id {to_wallet.id} doesn't belong to you"

    # Transaction from_wallet and to_wallet are equal
    from_wallet = create_random_wallet(db, owner_id=owner_id, balance=100)
    body = {"amount": 100, "from_wallet_id": from_wallet.id, "to_wallet_id": from_wallet.id}
    response = client.post(
        f"{settings.API_V1_STR}/transaction/", headers=user_token_headers, json=body
    )
    assert response.status_code == 400
    error = response.json()['detail']
    assert error == "To and from wallets must be different"


def test_create_transaction(
        client: TestClient, db: Session, user_token_headers: dict,
) -> None:
    owner_id = client.get(
        f"{settings.API_V1_STR}/user/whoami", headers=user_token_headers,
    ).json()['id']
    from_wallet = create_random_wallet(db, owner_id=owner_id, balance=100)
    to_wallet = create_random_wallet(db)

    body = {"amount": 100, "from_wallet_id": from_wallet.id, "to_wallet_id": to_wallet.id}
    response = client.post(
        f"{settings.API_V1_STR}/transaction/", headers=user_token_headers, json=body
    )
    assert response.status_code == 200
    content = response.json()
    assert content["amount"] == 100
    assert content["from_wallet_id"] == from_wallet.id
    assert content["to_wallet_id"] == to_wallet.id
    assert "id" in content
    assert "date" in content

    response = client.get(
        f"{settings.API_V1_STR}/wallet/", headers=user_token_headers
    )
    assert response.status_code == 200
    content = response.json()
    assert content["balance"] == from_wallet.balance - 100
