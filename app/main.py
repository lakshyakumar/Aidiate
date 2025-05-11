from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from app.src.routes.aidiate import router as aidiate_router
from app.src.routes.ideas_db import router as ideas_db_router

# Create FastAPI app instance
app = FastAPI(title="Aidiate Agent", description="Your Own AI Lean-Stack Service", version="1.0.0")

# Health check endpoint
@app.get("/health")
def health_check():
    """
    Health check endpoint to verify if the service is running.
    """
    return {"status": "ok", "message": "Service is running"}

@app.get("/", summary="AIdiate: your Lean-stack Companion", description="Provide out of the box AI capabilities to your idea and brainstorming.")
def project_intro():
    return {
        "project_name": "Aidiate",
        "description": "Provide out of the box AI capabilities to your idea and brainstorming.",
        "version": "1.0.0",
        "features": [
            "Fetch and stores your ideas",
            "Health check endpoint"
        ],
        "author": "Lakshya Kumar",
        "contact": "lklsquare@gmail.com"
    }

# Include the router
app.include_router(aidiate_router, prefix="/aidiate", tags=["Aidiate"])
app.include_router(ideas_db_router, prefix="/ideas", tags=["Ideas DB"])


# Run the application (if running directly)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
