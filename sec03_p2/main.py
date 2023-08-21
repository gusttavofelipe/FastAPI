from fastapi import FastAPI
from sec03_p2.routes import course_router, user_router


app = FastAPI()

app.include_router(course_router.router, tags=['courses'])
app.include_router(user_router.router, tags=['users'])


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(
        'main:app', host='0.0.0.0',
        port=8000, debug=True, reload=True
    )
