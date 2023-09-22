from fastapi import APIRouter, status, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.artclie_model import ArticleModel
from models.user_model import UserModel

from schemas.article_schema import ArticleSchema
from core.deps import get_session, get_current_user


router = APIRouter()


# POST
@router.post('/', status_code=status.HTTP_201_CREATED)
async def post_article(
    article: ArticleSchema,
    loged_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)
) -> ArticleSchema:

    new_article: ArticleModel = ArticleModel(
        title=article.title, description=article.description,
        url_font=article.url_font, user_id=loged_user.id
    )

    db.add(new_article)
    await db.commit()

    return new_article


# GET ARTICLES
@router.get('/')
async def get_articles(
        db: AsyncSession = Depends(get_session)) -> list[ArticleSchema]:

    async with db as session:
        query = select(ArticleModel)
        result = await session.execute(query)
        articles: list[ArticleModel] = result.scalars().unique().all()

        return articles


# GET ARTICLES
@router.get('/{article_id}')
async def get_articles(
        article_id: int, db: AsyncSession = Depends(get_session)
) -> ArticleSchema:

    async with db as session:
        query = select(ArticleModel).filter(ArticleModel.id == article_id)
        result = await session.execute(query)
        article: ArticleModel = result.scalars().unique().one_or_none()

        if article:
            return article
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'article with id {article_id} not found'
            )


# PUT ARTICLE
@router.put('/{article_id}')
async def put_article(
    article: ArticleSchema, article_id: int,
    db: AsyncSession = Depends(get_session),
    loged_user: UserModel = Depends(get_current_user)
) -> ArticleSchema:

    async with db as session:
        query = select(ArticleModel)\
            .filter(ArticleModel.id == article_id)\
            .filter(ArticleModel.user_id == loged_user.id)

        result = await session.execute(query)
        article_up: ArticleModel = result.scalars(
        ).unique().one_or_none()

        if article_up:
            if article.title:
                article_up.title = article.title
            if article.description:
                article_up.description = article.description
            if article.url_font:
                article_up.url_font = article.url_font
            if loged_user.id != article_up.user_id:
                article_up.user_id = loged_user.id

            await session.commit()

            return article_up
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'article with id {article_id} not found'
            )


# DELETE ARTICLE
@router.delete('/{article_od}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_articles(
        article_id: int, db: AsyncSession = Depends(get_session),
        loged_user: UserModel = Depends(get_current_user)
) -> ArticleSchema:

    async with db as session:
        query = select(ArticleModel)\
            .filter(ArticleModel.id == article_id)\
            .filter(ArticleModel.user_id == loged_user.id)

        result = await session.execute(query)
        article_del: ArticleModel = result.scalars().unique().one_or_none()

        if article_del:
            await session.delete()
            await session.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'article with id {article_id} not found'
            )
