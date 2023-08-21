from typing import Optional, Any
from time import sleep
from fastapi.responses import JSONResponse, Response
from sec03.models import Course, courses
from fastapi import (
    FastAPI, HTTPException, Depends, Path, Query, Header, status
)

app = FastAPI(
    # docs customization
    title='API de cursos',
    description='API para estudo',
    version='0.0.1'
)


def fake_db():
    try:
        print('opening database connection...')
        sleep(1)
    finally:
        print('closing database connection...')
        sleep(1)


@app.get(
    '/courses', summary='Return all courses',
    description='Return all courses or a empty dictionary',
    response_model=list[Course])
async def get_courses(db: Any = Depends(fake_db)):
    return courses
# Depends adiciona uma dependencia a um recurso
# (executa algo antes de chamar o recurso)


@app.get(
    '/courses/{course_id}',
    description='Return a course from a course dictionary',
    response_model=Course)
async def get_course(
        db: Any = Depends(fake_db),
        course_id: int = Path(
        default=None, title='Course id',  # title - in the docs
        description='Must be between 1 e 2', gt=0, lt=3)):  # descripition - in the docs
    try:
        course = courses[course_id]
        course.update({'id': course_id})  # adicionando id ao dict
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='course not found'
        )
    return course
# por padrão o status_code para post é 200


@app.post(
    '/courses',
    status_code=status.HTTP_201_CREATED,
    description='add a course in the dictionary',
    response_model=list[dict])
async def post(course: Course, db: Any = Depends(fake_db)):
    course_id = len(courses) + 1
    courses[course_id] = course
    course.id = course_id
    return course


@app.put('/courses/{course_id}', description='update a course')
async def put(course: Course, course_id: int, db: Any = Depends(fake_db)):
    if course_id in courses:
        courses[course_id] = course
        course.id = course_id

        return course
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'course with id {course_id} not exists'
        )


@app.delete('/courses/{course_id}', description='delete a course')
async def delete(course_id: int, db: Any = Depends(fake_db)):
    if course_id in courses:
        del courses[course_id]
        # return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'course with id {course_id} not exists'
        )


# Query and Header parameters

@app.get('/calculator')
async def calculate(
    a: int = Query(default=None, gt=5),
    b: int = Query(default=None, gt=10),
    c: Optional[int] = None,
        x_param: str = Header(default=None)):

    print(f'x_param: {x_param}')
    values_sum = a + b
    if c:
        values_sum += c
    return {'result': values_sum}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(
        'main:app', host='0.0.0.0',
        port=8000, debug=True, reload=True
    )
