from fastapi import FastAPI

from routers.dashboard import router

app = FastAPI()
app.include_router(router)
