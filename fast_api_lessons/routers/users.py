from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from typing import List

import crud
from database import get_db
from schemas import UserCreate, UserResponse, UserUpdate


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("", response_model=List[UserResponse])
def get_all_users(
    db: Session = Depends(get_db)
) -> list[UserResponse]:
    return crud.get_all_users(db)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
) -> UserResponse:
    user = crud.get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user


@router.post("/", response_model=UserResponse)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
) -> UserResponse:

    if crud.get_user_by_email(db, user.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with email {user.email} already exists"
        )

    return crud.create_user(db, user)


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db)
) -> UserResponse:

    updated_user = crud.update_user(
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


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
) -> Response:

    deleted_user = crud.delete_user(db, user_id)

    if deleted_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)

