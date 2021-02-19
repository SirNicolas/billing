from sqlalchemy.orm import Session

from app.common.wallet import crud, schema
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_float


def test_create_wallet(db: Session) -> None:
    user = create_random_user(db)
    wallet = crud.wallet.create(db=db, owner_id=user.id)
    assert wallet.balance == 0
    assert wallet.owner_id == user.id


def test_get_wallet(db: Session) -> None:
    user = create_random_user(db)
    wallet = crud.wallet.create(db=db, owner_id=user.id)
    stored_wallet = crud.wallet.get(db=db, owner_id=user.id)
    assert stored_wallet
    assert wallet.id == stored_wallet.id
    assert wallet.owner_id == stored_wallet.owner_id
    assert wallet.balance == stored_wallet.balance


def test_update_wallet(db: Session) -> None:
    user = create_random_user(db)
    wallet = crud.wallet.create(db=db, owner_id=user.id)
    balance2 = random_float()
    wallet_update = schema.WalletUpdate(balance=balance2)
    wallet2 = crud.wallet.update(db=db, db_obj=wallet, obj_in=wallet_update)
    assert wallet.id == wallet2.id
    assert wallet2.balance == balance2
    assert wallet.owner_id == wallet2.owner_id
