import datetime

from sqlalchemy import Column, ForeignKey, Integer, Float, DateTime
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class Wallet(Base):
    id = Column(Integer, primary_key=True, index=True)
    balance = Column(Float, default=0)

    owner_id = Column(Integer, ForeignKey("user.id"), index=True, unique=True)
    owner = relationship("User", back_populates="wallet")

    to_transactions = relationship("Transaction", back_populates="to_wallet",
                                   foreign_keys='Transaction.to_wallet_id')
    from_transactions = relationship("Transaction", back_populates="from_wallet",
                                     foreign_keys='Transaction.from_wallet_id')


class Transaction(Base):
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    amount = Column(Float)

    to_wallet_id = Column(Integer, ForeignKey("wallet.id"), index=True)
    to_wallet = relationship(Wallet, back_populates="to_transactions", foreign_keys=to_wallet_id)

    from_wallet_id = Column(Integer, ForeignKey("wallet.id"), index=True)
    from_wallet = relationship(Wallet, back_populates="from_transactions", foreign_keys=from_wallet_id)
