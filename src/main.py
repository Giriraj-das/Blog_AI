from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from auth import router as auth_router
from user import router as user_router
# from post import router as post_router
# from comment import router as comment_router
from core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


main_app = FastAPI(
    lifespan=lifespan,
    default_response_class=ORJSONResponse,
    title='Blog_AI',
    description='FastAPI, PostgreSQL, SQLAlchemy(v2), Docker, Pytest, Google AI API (checks posts and comments for '
                'profanity)',
)
main_app.include_router(auth_router)
main_app.include_router(user_router)
# main_app.include_router(post_router)
# main_app.include_router(comment_router)

if __name__ == '__main__':
    uvicorn.run(
        'main:main_app',
        host=settings.run.host,
        port=settings.run.port,
        reload=True
    )
