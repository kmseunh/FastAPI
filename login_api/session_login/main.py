from fastapi import FastAPI

from api import auth, some_resource

app = FastAPI()


app.include_router(auth.router)
app.include_router(some_resource.router)
