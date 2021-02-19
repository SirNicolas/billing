from typing import Optional, List

from sqlalchemy.orm import Session

from app.common.wallet import crud, model, schema
from app.tests.utils.user import create_random_user


def create_random_wallet(
        db: Session, owner_id: Optional[int] = None, balance: float = None
) -> model.Wallet:
    if not owner_id:
        owner_id = create_random_user(db).id
    wallet = crud.wallet.get(db, owner_id=owner_id)
    if not wallet:
        wallet = crud.wallet.create(db=db, owner_id=owner_id)
    if balance:
        wallet = crud.wallet.update(db, wallet, schema.WalletUpdate(balance=balance))
    return wallet


def create_transactions(db: Session, owner_id: int) -> List[model.Transaction]:
    wallet1 = create_random_wallet(db, owner_id)
    crud.wallet.update(db, wallet1, schema.WalletUpdate(balance=10))

    user2 = create_random_user(db)
    wallet2 = create_random_wallet(db, user2.id)

    transaction_in = schema.TransactionCreate(
        amount=10, from_wallet_id=wallet1.id, to_wallet_id=wallet2.id
    )
    transaction1 = crud.wallet.create_transaction(db, wallet1, transaction_in)

    transaction_in = schema.TransactionCreate(
        amount=10, from_wallet_id=wallet2.id, to_wallet_id=wallet1.id
    )
    transaction2 = crud.wallet.create_transaction(db, wallet2, transaction_in)
    return [transaction1, transaction2]
