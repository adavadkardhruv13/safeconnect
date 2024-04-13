from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from models.db import get_pool, CreateVehicleRegisterationTable
from routes.submission import submission
import logging
import os
from dotenv import load_dotenv

load_dotenv()



cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME")
api_key = os.getenv("CLOUDINARY_API_KEY")
api_secret = os.getenv("CLOUDINARY_API_SECRET")

# Configure Cloudinary
import cloudinary.uploader
cloudinary.config(
    cloud_name=cloud_name,
    api_key=api_key,
    api_secret=api_secret
)


app = FastAPI(
    title="Safeconnect Server",
    description="An Application"
)

# Configure CORS middleware
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Include routers
app.include_router(submission.router)

# Setup database connection pool on application startup
@app.on_event("startup")
async def startup_event():
    pool = await get_pool()
    table_creator = CreateVehicleRegisterationTable(pool)
    await table_creator.create_vehicle_registration_table()

# Close database connection pool on application shutdown
@app.on_event("shutdown")
async def shutdown_event():
    await app.state.pool.close()
    logging.info("Database connection pool closed")

# Example index endpoint
@app.get("/")
async def index(request: Request):
    return {"message": "Hello, FastAPI!"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)