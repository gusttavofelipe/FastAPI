from typing import Optional
from fastapi.responses import JSONResponse, Response
from sec03.models import Course
from fastapi import (
    FastAPI, HTTPException, Path, Query, Header, status
)

app = FastAPI()

courses = {
    1: {
        'title': 'Course 1',
        'classes': 112,
        'hours': 12
    },
    2: {
        'title': 'Course 2',
        'classes': 12,
        'hours': 3
    },
    3: {
        'title': 'Course 3',
        'classes': 117,
        'hours': 13
    },
}


@app.get('/courses')
async def get_courses():
    return courses


@app.get('/courses/{course_id}')  # todo input vem como str
async def get_course(course_id: int = Path(
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


@app.post('/courses', status_code=status.HTTP_201_CREATED)
async def post(course: Course):
    course_id = len(courses) + 1
    courses[course_id] = course
    course.id = course_id
    return course


@app.put('/courses/{course_id}')
async def put(course: Course, course_id: int):
    if course_id in courses:
        courses[course_id] = course
        course.id = course_id

        return course
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'course with id {course_id} not exists'
        )


@app.delete('/courses/{course_id}')
async def delete(course_id: int):
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
