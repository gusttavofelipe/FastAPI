from fastapi import (
    APIRouter, HTTPException, Response, Depends, status
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from models.course_model import CourseModel
from core.deps import get_session

router = APIRouter()


# POST
@router.post(
    '/', status_code=status.HTTP_201_CREATED,
    response_model=CourseModel)
async def post(
        course: CourseModel,
        db: AsyncSession = Depends(get_session)):

    new_course = CourseModel(
        title=course.title, number_classes=course.number_classes,
        hours=course.hours)

    db.add(new_course)
    await db.commit()
    return new_course


# GET COURSES
@router.get('/', response_model=list[CourseModel])
async def get_courses(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CourseModel)
        result = await session.execute(query)
        courses: list[CourseModel] = result.scalars().all()

        return courses


# GET COURSE
@router.get('/{course_id}', response_model=CourseModel, status_code=status.HTTP_200_OK)
async def get_courses(course_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CourseModel).filter(CourseModel.id == course_id)
        result = await session.execute(query)
        course: CourseModel = result.scalar_one_or_none()
        if course:
            return course
        else:
            raise HTTPException(
                detail=f'course with id {course_id} not found',
                status_code=status.HTTP_404_NOT_FOUND
            )


@router.put('/{course_id}', response_model=CourseModel)
async def put(
        course_id: int, course_upd: CourseModel,
        db: AsyncSession = Depends(get_session)):

    async with db as session:
        query = select(CourseModel).filter(CourseModel.id == course_id)
        result = await session.execute(query)
        course: CourseModel = result.scalar_one_or_none()

        if course:
            course.title = course_upd.title
            course.hours = course_upd.hours
            course.number_classes = course_upd.number_classes
            await session.commit()

            return course_upd
        else:
            raise HTTPException(
                detail=f'course with id {course_id} not found',
                status_code=status.HTTP_404_NOT_FOUND
            )


@router.delete('/{course_id}', response_model=CourseModel)
async def delete(course_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CourseModel).filter(CourseModel.id == course_id)
        result = await session.execute(query)
        course_del = result.scalar_one_or_none()

        if course_del:
            await session.delete(course_del)
            await session.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(
                detail=f'course with id {course_id} not found',
                status_code=status.HTTP_404_NOT_FOUND
            )
