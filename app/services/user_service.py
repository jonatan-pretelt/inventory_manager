from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app import models
from app.exceptions import DuplicateUserError
from app.core import security
import logging

logger = logging.getLogger(__name__)

def create_user(db: Session, email: str, password: str):
    user = models.UserDB(email=email,hashed_password = security.hash_password(password))
    db.add(user)

    try:
        db.flush()
    except IntegrityError:
        logger.warning("Duplicate User attempted", extra={"email": user.email})
        raise DuplicateUserError("User already exists")

    return user