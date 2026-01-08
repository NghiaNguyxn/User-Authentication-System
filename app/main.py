from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import create_db_and_table
from app.config import settings
from app.api import auth, user
from app.exception_handlers import register_exception_handlers

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("System is starting up...")
    create_db_and_table()

    yield

    print("System is shutting down...")

app = FastAPI(
    title="User Authentication System",
    description="A complete user authentication system with FastAPI",
    version="1.0.0",
    lifespan=lifespan
)

# Register all exception handlers
register_exception_handlers(app)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Health check endpoint
@app.get("/")
async def root():
    return {"message": "User Authentication System API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Include the APIRouters
app.include_router(auth.router)
app.include_router(user.router)