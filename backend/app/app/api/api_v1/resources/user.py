from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import utils
from app.common.user import crud, model, schema

router = APIRouter()


@router.post("/", response_model=schema.User)
def create_user(
        user_in: schema.UserCreate,
        db: Session = Depends(utils.get_db),
) -> Any:
    """
    Create new user.
    """
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = crud.user.create(db, obj_in=user_in)
    return user


@router.get("/whoami", response_model=schema.User)
def get_user(
        current_user: model.User = Depends(utils.get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return current_user
