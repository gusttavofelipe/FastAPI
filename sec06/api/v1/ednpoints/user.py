from typing import Optional
from fastapi import APIRouter, HTTPException, Response, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.user_model import UserModel
from schemas.user_schema import (
    UserSchemaBase, UserSchemaCreate, UserSchemaUpdate, UserSchemaArticles
)
from core.deps import get_session, get_current_user
from core.security import generate_password_hash
from core.auth import autenticate, _create_token_acess
from sqlalchemy.exc import IntegrityError


router = APIRouter()


# GET LOGADO
@router.get('/logged')
def get_logged_user(logged_user: UserModel = Depends(get_current_user)):
    return logged_user


# POST / Sing up
@router.post('/singup', status_code=status.HTTP_201_CREATED)
async def post_user(user: UserSchemaCreate, db: AsyncSession = Depends(get_session)):
    new_user: UserModel = UserModel(
        name=user.name, lastname=user.lastname, email=user.email,
        password=generate_password_hash(user.password), is_admin=user.is_admin
    )
    async with db as session:
        try:
            session.add(new_user)
            await session.commit()

            return new_user
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail='email already exists'
            )


@router.get('/')
async def get_users(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UserModel)
        resul = await session.execute(query)
        user: list[UserSchemaBase] = resul.scalars().unique().all()

        return user


@router.get('/{user_id}')
async def get_user(user_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UserModel).filter(UserModel.id == user_id)
        result = await session.execute(query)
        user: UserSchemaArticles = result.scalars().unique().one_or_none()

        if user:
            return user

        raise HTTPException(
            detail=f'user with id {user_id} not found',
            status_code=status.HTTP_404_NOT_FOUND
        )


@router.put('/{user_id}', status_code=status.HTTP_202_ACCEPTED)
async def put_user(
        user_id: int, user: UserSchemaUpdate,
        db: AsyncSession = Depends(get_session)
):
    async with db as session:
        query = select(UserModel).filter(UserModel.id == user_id)
        result = await session.execute(query)
        user_update: UserSchemaBase = result.scalars().unique().one_or_none()

        if user_update:
            if user.name:
                user_update.name = user.name
            if user.lastname:
                user_update.lastname = user.lastname
            if user.email:
                user_update.email = user.email
            if user.password:
                user_update.password = generate_password_hash(user.password)
            if user.is_admin:
                user_update.is_admin = user.is_admin

            await session.commit()
            return user_update

        raise HTTPException(
            detail=f'user with id {user_id} not found',
            status_code=status.HTTP_404_NOT_FOUND
        )


@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UserModel).filter(UserModel.id == user_id)
        result = await session.execute(query)
        user_del: UserSchemaArticles = result.scalars().unique().one_or_none()

        if user_del:
            await session.delete(user_del)
            await session.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)

        raise HTTPException(
            detail=f'user with id {user_id} not found',
            status_code=status.HTTP_404_NOT_FOUND
        )


@router.post('/login')
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_session)
):
    user = await autenticate(email=form_data.username, password=form_data.password, db=db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='incorrect access data'
        )
    return JSONResponse(
        content={'acess_token': _create_token_acess(sub=user.id),
                 'token_type': 'bearer'}, status_code=status.HTTP_200_OK
    )
