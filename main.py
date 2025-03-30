from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from features.routes import router as scrapin_enhancement  # Updated name for clarity

# FastAPI app instance
app = FastAPI(title="LinkedIn Profile Enhancement API", version="1.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (can be restricted for security)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Include router (renamed for clarity)
app.include_router(scrapin_enhancement, prefix="/api")

# Root endpoint
@app.get("/")
def root():
    return {"message": "Welcome to the LinkedIn Profile Enhancement API powered by Scrapin.io!"}

# Main entry point
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9100, reload=True)
