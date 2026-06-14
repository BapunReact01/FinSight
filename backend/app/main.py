from fastapi import FastAPI
from app.api import auth_router, companies_router, transactions_router, analytics_router, files_router
from app.core.database import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FinSight API",
    description="AI Financial Analytics Platform",
    version="1.0.0"
)

# Include routers
app.include_router(auth_router)
app.include_router(companies_router)
app.include_router(transactions_router)
app.include_router(analytics_router)
app.include_router(files_router)

@app.get("/")
def home():
    return {
        "message": "Welcome to FinSight API",
        "status": "Running",
        "version": "1.0.0"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}