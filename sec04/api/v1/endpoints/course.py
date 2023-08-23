from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.course_model import CourseModel
from schemas.course_schema import CourseSchema
from core.deps import get_session

router = APIRouter()


@router.post('/', status_code=status.HTTP_201_CREATED,)
async def post_course(
    course: CourseSchema,
    db: AsyncSession = Depends(get_session)
) -> CourseSchema:

    new_course = CourseModel(
        title=course.title,
        number_classes=course.number_classes,
        hours=course.hours)

    db.add(new_course)
    await db.commit()
    return new_course


@router.get('/')
async def get_courses(
    db: AsyncSession = Depends(get_session)
) -> list[CourseSchema]:

    async with db as session:
        query = select(CourseModel)
        result = await session.execute(query)
        courses: list(CourseModel) = result.scalars().all()

        return courses


@router.get('/{course_id}')
async def get_course(
    course_id: int, db: AsyncSession = Depends(get_session)
) -> CourseSchema:

    async with db as session:
        query = select(
            CourseModel).filter(CourseModel.id == course_id
                                )
    result = await session.execute(query)
    course = result.scalar_one_or_none()

    if course:
        return course
    else:
        raise HTTPException(
            detail=f'course with id {course_id} not found',
            status_code=status.HTTP_404_NOT_FOUND
        )


@ router.put('/{course_id}')
async def put_course(
    course_id: int, course_upd: CourseSchema,
      db: AsyncSession = Depends(get_session)
      ) -> CourseSchema:

    async with db as session:
        query = select(
            CourseModel).filter(CourseModel.id == course_id
                                )
    result = await session.execute(query)
    course = result.scalar_one_or_none()

    if course:
        course.title = course_upd.title
        course.number_classes = course_upd.number_classes
        course.hours = course_upd.hours

        await session.commit()
        return course_upd
    else:
        raise HTTPException(
            detail=f'course with id {course_id} not found',
            status_code=status.HTTP_404_NOT_FOUND
        )


@ router.delete('/{course_id}')
async def delete_course(
    course_id: int,
      db: AsyncSession = Depends(get_session)
      ) -> CourseSchema:

    async with db as session:
        query = select(
            CourseModel).filter(CourseModel.id == course_id
                                )
    result = await session.execute(query)
    course_del = result.scalar_one_or_none()

    if course_id:
        await session.delete(course_del)
        await session.commit()

        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(
            detail=f'course with id {course_id} not found',
            status_code=status.HTTP_404_NOT_FOUND
        )