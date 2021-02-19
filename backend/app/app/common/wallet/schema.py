from datetime import datetime
from pydantic import BaseModel, validator


# Shared properties
class WalletBase(BaseModel):
    pass


# Properties to receive on wallet update
class WalletUpdate(WalletBase):
    balance: float

    @validator('balance')
    def must_be_ge_than_zero(cls, v):
        if v <= 0:
            raise ValueError('balance must be positive')
        return v


# Properties shared by models stored in DB
class WalletInDBBase(WalletBase):
    id: int
    owner_id: int
    balance: float

    class Config:
        orm_mode = True


# Properties to return to client
class Wallet(WalletInDBBase):
    pass


# Shared properties
class TransactionBase(BaseModel):
    amount: float
    to_wallet_id: int
    from_wallet_id: int


# Properties to receive on wallet creation
class TransactionCreate(TransactionBase):
    pass


# Properties shared by models stored in DB
class Transaction(TransactionBase):
    id: int
    date: datetime

    class Config:
        orm_mode = True
