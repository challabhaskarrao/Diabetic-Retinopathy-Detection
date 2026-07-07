from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.router import router

app = FastAPI(
    title="Diabetic Retinopathy AI Pipeline API",
    description="End-to-End PyTorch DR Pipeline with FastAPI Backend",
    version="1.0.0"
)

# Configure CORS for React frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace with specific frontend URLs (e.g. localhost:5173, localhost:3000)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the main router
app.include_router(router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    # Run server locally for development
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
