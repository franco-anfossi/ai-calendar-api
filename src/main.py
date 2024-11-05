from fastapi import FastAPI

from .calendar.routes import router as calendar_router
from .event.routes import router as event_router
from .middleware import setup_cors
from .user.routes import router as user_router

app = FastAPI()

setup_cors(app)

app.include_router(user_router)
app.include_router(calendar_router)
app.include_router(event_router)


@app.get("/")
async def read_root():
    return {"message": "Welcome to the API!"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
