from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api import utils
from app.core import security
from app.common.user import crud, schema

router = APIRouter()


@router.post("/login", response_model=schema.Token)
def login(
        db: Session = Depends(utils.get_db),
        form_data: OAuth2PasswordRequestForm = Depends(),
) -> Any:
    user = crud.user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=401, detail="Inactive user")
    return {
        "access_token": security.create_access_token(user.id),
        "token_type": "bearer",
    }
