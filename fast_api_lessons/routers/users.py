from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session

from authorization import require_roles
from constants import UserRole
import db.crud_user as crud_user
from db.database import get_db
from db.models import User
from schemas import UserResponse, UserUpdate


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("", response_model=list[UserResponse])
def get_all_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.SYSADMIN))
) -> list[UserResponse]:
    """Get all users"""
    return crud_user.get_all_users(db)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.SYSADMIN))
) -> UserResponse:
    """Get single user by ID"""
    user = crud_user.get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.SYSADMIN))
) -> UserResponse:
    """Update a user"""

    updated_user = crud_user.update_user(
        db,
        user_id,
        user
    )

    if updated_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} does not exist"
        )

    return updated_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.SYSADMIN))
) -> Response:
    """Delete a user"""

    deleted_user = crud_user.delete_user(db, user_id)

    if deleted_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
