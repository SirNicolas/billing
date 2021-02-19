from sqlalchemy.orm import Session

from app.db import base  # noqa: F401
from app.db.session import engine
from app.db.base_class import Base
from app.core.config import settings
from app.common.user import crud, schema


def init_db(db: Session, local_engine=None) -> None:
    Base.metadata.create_all(bind=local_engine or engine)

    user = crud.user.get_by_email(db, email=settings.TEST_USER)
    if not user:
        user_in = schema.UserCreate(
            email=settings.TEST_USER,
            password=settings.TEST_USER_PASS,
            is_superuser=True,
        )
        user = crud.user.create(db, obj_in=user_in)  # noqa: F841
