from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import utils
from app.common.exceptions import WalletBalanceException, WalletPermissionException, WalletTransactionException
from app.common.user.model import User
from app.common.wallet import crud, schema

router = APIRouter()


@router.post("/", response_model=schema.Transaction)
def create_transaction(
        transaction_in: schema.TransactionCreate,
        db: Session = Depends(utils.get_db),
        current_user: User = Depends(utils.get_current_active_user),
) -> Any:
    """
    Create transaction.
    """
    wallet = crud.wallet.get(db=db, owner_id=current_user.id)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    try:
        wallet = crud.wallet.create_transaction(db=db, from_wallet=wallet, obj_in=transaction_in)
    except (WalletBalanceException, WalletPermissionException, WalletTransactionException) as e:
        raise HTTPException(status_code=400, detail=str(e))
    return wallet


@router.get("/", response_model=List[schema.Transaction])
def get_transactions(
        db: Session = Depends(utils.get_db),
        current_user: User = Depends(utils.get_current_active_user),
) -> Any:
    """
    Get user transactions.
    """
    wallet = crud.wallet.get(db=db, owner_id=current_user.id)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    transactions = crud.wallet.get_transactions(db=db, wallet_id=wallet.id)
    return transactions
