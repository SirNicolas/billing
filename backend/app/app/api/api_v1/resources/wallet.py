from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import utils
from app.common.user.model import User
from app.common.wallet import crud, schema

router = APIRouter()


@router.post("/", response_model=schema.Wallet)
def create_wallet(
        db: Session = Depends(utils.get_db),
        current_user: User = Depends(utils.get_current_active_user),
) -> Any:
    """
    Create a wallet for user.
    """
    wallet = crud.wallet.get(db=db, owner_id=current_user.id)
    if not wallet:
        wallet = crud.wallet.create(db=db, owner_id=current_user.id)
    else:
        raise HTTPException(status_code=400, detail="You already have wallet")

    return wallet


@router.patch("/", response_model=schema.Wallet)
def update_wallet(
        wallet_in: schema.WalletUpdate,
        db: Session = Depends(utils.get_db),
        current_user: User = Depends(utils.get_current_active_user),
) -> Any:
    """
    Add user's wallet balance from external resource
    """
    wallet = crud.wallet.get(db=db, owner_id=current_user.id)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    wallet = crud.wallet.update(db=db, db_obj=wallet, obj_in=wallet_in)
    return wallet


@router.get("/", response_model=schema.Wallet)
def get_wallet(
        db: Session = Depends(utils.get_db),
        current_user: User = Depends(utils.get_current_active_user),
) -> Any:
    """
    Get user wallet.
    """
    wallet = crud.wallet.get(db=db, owner_id=current_user.id)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return wallet
