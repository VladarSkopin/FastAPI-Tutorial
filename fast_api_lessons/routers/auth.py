from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from config import TOKEN_EXPIRE_MINUTES
import db.crud_auth as crud_auth
from db.database import get_db
from dependencies import get_current_active_user
from db.models import User
from logging_config import get_logger
from schemas import Token, UserCreate, UserResponse
from security import create_access_token


logger = get_logger(__name__)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# Auth Endpoints


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
) -> UserResponse:
    """
    Register a new user.
    """

    if crud_auth.get_user_by_email(db, user.email):
        logger.warning(
            "User with email=%s already exists",
            user.email
        )
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists"
        )

    logger.info(
        "Registered new user with email=%s",
        user.email
    )

    return crud_auth.create_user(db, user)


@router.post(
    "/token",
    response_model=Token
)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
) -> Token:
    """
    Authenticate a user and return a JWT token.
    """

    logger.info(
        "Login attempt email=%s (username)",
        form_data.username
    )

    user = crud_auth.authenticate_user(
        db,
        form_data.username,
        form_data.password
    )

    if user is None:
        logger.warning(
            "Failed login email=%s",
            form_data.username
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )

    logger.info(
        "Login successful email=%s",
        user.email
    )

    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    )

    logger.info(
        "Generated new token for email=%s",
        user.email
    )

    return Token(
        access_token=access_token,
        token_type="bearer"
    )


@router.get(
    "/profile",
    response_model=UserResponse
)
def get_profile(
    current_user: User = Depends(get_current_active_user)
) -> UserResponse:
    """
    Return the currently authenticated user.
    """

    logger.info(
        "Get profile for current user with email=%s",
        current_user.email
    )

    return current_user


@router.get("/verify-token")
def verify_token_endpoint(
    current_user: User = Depends(get_current_active_user)
):
    """
    Verify that the supplied JWT is valid.
    """

    logger.info("Verify that the supplied JWT is valid")

    return {
        "valid": True,
        "user": {
            "id": current_user.id,
            "name": current_user.name,
            "email": current_user.email,
            "role": current_user.role,
            "is_active": current_user.is_active,
        },
    }
