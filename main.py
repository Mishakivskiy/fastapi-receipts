from fastapi import FastAPI
from core.config import Settings
from starlette.middleware.cors import CORSMiddleware

from core.database import Base, engine

from app.routes.user_router import user_router
from app.routes.receipt_router import receipt_router

Base.metadata.create_all(bind=engine)

settings = Settings()
app = FastAPI()

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            str(origin).strip("/") for origin in settings.BACKEND_CORS_ORIGINS
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(user_router, prefix='/api/users')
app.include_router(receipt_router, prefix='/api/receipts')


@app.get("/")
def read_root():
    return {"message": "Welcome to the Receipt Management API"}

