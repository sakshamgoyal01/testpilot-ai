# backend/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import routers
from backend.routers import dashboard, test_gen, run_tests, code_reviews
from backend.routers.test_gen import router

app = FastAPI(
    title="TestPilot - AI SaaS Testing Backend",
    description="Modular backend with endpoints for generation, execution, analytics and AI insights.",
    version="1.0.0"
)

# CORS Middleware (adjust in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with frontend domain in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routers with relevant tags
app.include_router(dashboard.router, prefix="/api", tags=["Dashboard Metrics"])
app.include_router(test_gen.router, prefix="/api", tags=["Test Generation"])
app.include_router(run_tests.router, prefix="/api", tags=["Test Execution"])
app.include_router(code_reviews.router, prefix="/api", tags=["Code Review & Risk Scoring"])

# Root health check
@app.get("/")
def root():
    return {"status": "✅ TestPilot API is up", "endpoints": ["/api/metrics", "/api/generate", "/api/run", "/api/review"]}
