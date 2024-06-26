from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api import auth, some_resource, user_router

app = FastAPI()


origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(some_resource.router)
app.include_router(user_router.router)
