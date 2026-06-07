"""
avry-workflows Microservice Entry Point
Description: N8N workflow integration
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="AVRY Workflows Service",
    description="N8N workflow integration",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and include routes
try:
    from app.routes.workflows import router as workflows_router
    app.include_router(workflows_router)
    print("[✓] Workflow routes registered")
except Exception as e:
    print(f"[!] Warning: Could not import workflow routes: {e}")
try:
    from app.routes.n8n import router as n8n_router
    app.include_router(n8n_router)
    print("[✓] N8N routes registered")
except Exception as e:
    print(f"[!] Warning: Could not import n8n routes: {e}")
try:
    from app.routes import *
    # Include routers here as needed
except Exception as e:
    print(f"Warning: Could not import routes: {e}")

# Health check endpoint
@app.get("/health")
async def health():
    """Service health check"""
    return {
        "status": "healthy",
        "service": "avry-workflows",
        "version": "1.0.0"
    }

@app.get("/")
async def root():
    """Service info"""
    return {
        "service": "AVRY Workflows Service",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8088"))
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        reload=os.getenv("ENVIRONMENT", "production") == "development"
    )
