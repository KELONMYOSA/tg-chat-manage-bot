from fastapi import FastAPI

from src.api.routers import user

app = FastAPI(
    title="Comfortel Chat Manage API",
    contact={"name": "KELONMYOSA", "url": "https://t.me/KELONMYOSA"},
    version="0.0.1",
    docs_url="/docs",
    redoc_url="/docs/redoc",
)

app.include_router(user.router)
