from fastapi import FastAPI

app = FastAPI(
    title="Project 1: FastAPI + SQL API",
    version="0.1.0",
    description="Backend API built with Python and FastAPI for the Projects_CV series."
)


@app.get("/health")
def health_check():
    """Health check endpoint to verify that the API is running."""
    return {"status": "ok", "message": "API running successfully"}


@app.get("/")
def root():
    """Root endpoint - returns a welcome message."""
    return {"hello": "world", "info": "Welcome to your first FastAPI project!"}