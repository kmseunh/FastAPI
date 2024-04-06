from fastapi import FastAPI

from app.api import router

app = FastAPI(
    title="Social Media App",
    description="Engine Behind Social Media App",
    version="0.1",
)

app.include_router(router)
