from fastapi import FastAPI
from app.db.session import Base, engine
from app.api.v1.users import router as users_router

app = FastAPI(
    title="Project 1: FastAPI + SQL API",
    version="0.2.0",
    description="Backend API built with Python, FastAPI and SQLAlchemy."
)

# Create database tables at startup (if they don`t exist)
Base.metadata.create_all(bind=engine)

@app.get("/health")
def health_check():
    """Health check endpoint to verify that the API is running."""
    return {"status": "ok", "message": "API running successfully"}

# Mount v1 routes
app.include_router(users_router)

@app.get("/")
def root():
    return {"hello": "world", "info": "Welcome to your FastAPI + SQL project!"}
