import asyncio
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import (
    admin,
    appointments,
    auth,
    availability,
    dashboard,
    doctors,
    patients,
    records,
)

# Updated 10 Jun to main.py
# day35-consolidation

app = FastAPI(
    title="Hospital Management System",
    version="2.0.0",
    description="HMS v2 — FastAPI + PostgreSQL + Azure",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["Health"])
def health_check():
    """
    Health check — does NOT touch the database.
    Returns 200 when the app process is running.
    """
    return {
        "status": "ok",
        "service": "Hospital Management System v2 - CI/CD Enabled",
        "version": "2.0.0",
        "environment": os.getenv("APP_ENV", "unknown"),
    }


app.include_router(auth.router, prefix="/auth", tags=["Auth"])

app.include_router(patients.router, prefix="/patients", tags=["Patients"])

app.include_router(doctors.router, prefix="/doctors", tags=["Doctors"])

app.include_router(appointments.router, prefix="/appointments", tags=["Appointments"])
app.include_router(availability.router, prefix="/doctors", tags=["Availability"])

app.include_router(dashboard.router, prefix="/patients", tags=["Dashboard"])

app.include_router(records.router, prefix="/patients", tags=["Medical Records"])

app.include_router(admin.router, prefix="/admin", tags=["Admin"])


@app.get("/")
def home():
    return {"message": "Hospital API Running"}


async def main():
    print("ALL OK")


if __name__ == "__main__":
    asyncio.run(main())
