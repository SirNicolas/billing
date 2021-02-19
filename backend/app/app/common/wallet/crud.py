from typing import Optional, List

from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from app.common.exceptions import WalletBalanceException, WalletPermissionException, WalletTransactionException
from app.common.wallet.model import Wallet, Transaction
from app.common.wallet.schema import WalletUpdate, TransactionCreate


class CRUDWallet:

    def update(
            self, db: Session, db_obj: Wallet, obj_in: WalletUpdate
    ) -> Wallet:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def create(
            self, db: Session, owner_id: int
    ) -> Wallet:
        db_obj = Wallet(owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get(
            self, db: Session, owner_id: int
    ) -> Optional[Wallet]:
        return db.query(Wallet).filter(Wallet.owner_id == owner_id).one_or_none()

    def get_by_id(
            self, db: Session, id: int
    ) -> Optional[Wallet]:
        return db.query(Wallet).filter(Wallet.id == id).one_or_none()

    def create_transaction(
            self, db: Session, from_wallet: Wallet, obj_in: TransactionCreate
    ) -> Transaction:
        if isinstance(obj_in, dict):
            data = obj_in
        else:
            data = obj_in.dict(exclude_unset=True)

        if from_wallet.id != data['from_wallet_id']:
            raise WalletPermissionException(
                f"Wallet with id {data['from_wallet_id']} doesn't belong to you"
            )
        if from_wallet.id == data['to_wallet_id']:
            raise WalletTransactionException("To and from wallets must be different")
        try:
            db_obj = Transaction(**data)

            to_wallet = self.get_by_id(db, db_obj.to_wallet_id)

            to_wallet.balance += db_obj.amount
            from_wallet.balance -= db_obj.amount

            if from_wallet.balance < 0:
                raise WalletBalanceException(
                    "Amount of money you want to send is greater than your wallet's balance"
                )

            db.add(db_obj)
            db.commit()
        except Exception:
            db.rollback()
            raise

        db.refresh(db_obj)
        db.refresh(to_wallet)
        db.refresh(from_wallet)

        return db_obj

    def get_transactions(
            self, db: Session, wallet_id: int
    ) -> List[Transaction]:
        return db.query(Transaction).filter(
            (Transaction.to_wallet_id == wallet_id) |
            (Transaction.from_wallet_id == wallet_id)
        ).all()


wallet = CRUDWallet()
