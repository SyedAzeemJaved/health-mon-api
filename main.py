from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi_pagination import add_pagination

# Auth
from routers import jwt_tokens

# Admin level routes
from routers.admin import (
    admins,
    associations,
    caretakers,
    doctors,
    patients,
    users,
    stats,
)

# Current user level routes - Non admin
## Current - Patient user level routes
from routers.current.patients import (
    actions as current_patient_actions,
    history as current_patient_history,
)

## Current - Caretaker and doctor user level routes
from routers.current.caretaker_and_doctor import (
    patients as current_caretaker_and_doctor_patients,
)

# Common user level routes
from routers.common import me as common_me

tags_metadata = [
    # Auth
    {
        "name": "auth",
        "description": "Create JWT based access tokens that use SHA256 enterprise level security.",
    },
    # Admin level routes
    {
        "name": "admin - users",
        "description": "Create, read, update and manage all users - Admin level routes.",
    },
    {
        "name": "admin - associations",
        "description": "Associate a patient to a caretaker or doctor - Admin level routes.",
    },
    {
        "name": "admin - admins",
        "description": "Read and fetch all admins - Admin level routes.",
    },
    {
        "name": "admin - caretakers",
        "description": "Read and fetch all caretakers - Admin level routes.",
    },
    {
        "name": "admin - doctors",
        "description": "Read and fetch all doctors - Admin level routes.",
    },
    {
        "name": "admin - patients",
        "description": "Read and fetch all patients - Admin level routes.",
    },
    {
        "name": "admin - stats",
        "description": "Get stats for the dashboard - Admin level routes.",
    },
    # Current level routes - Non admin
    ## Current - Patient user level routes
    {
        "name": "patient - actions",
        "description": "Post actions for current user - Patient level routes.",
    },
    {
        "name": "patient - history",
        "description": "Post history for current user - Patient level routes.",
    },
    ## Current - Caretaker and doctor user level routes
    {
        "name": "caretaker and doctor - patients",
        "description": "Read and fetch all patients for current user - Caretaker and doctor level routes.",
    },
    # Common user level routes
    {
        "name": "common - me",
        "description": "Manage current user - Common user level routes.",
    },
]
origins = [
    "*",
]

app = FastAPI(
    title="IoT Health Tracking System",
    description="Python FastAPI IoT based Health Tracking System for Immobilized Patients.",
    version="1.0.0",
    openapi_tags=tags_metadata,
    redoc_url=None,
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(jwt_tokens.router)
# Admin level routes
app.include_router(users.router)
app.include_router(associations.router)
app.include_router(admins.router)
app.include_router(caretakers.router)
app.include_router(doctors.router)
app.include_router(patients.router)
app.include_router(stats.router)
# Current user level routes - Non admin
## Current - Patient user level routes
app.include_router(current_patient_actions.router)
app.include_router(current_patient_history.router)
## Current - Caretaker and doctor user level routes
app.include_router(current_caretaker_and_doctor_patients.router)
# Common user level routes
app.include_router(common_me.router)

add_pagination(app)  # add pagination to your app
