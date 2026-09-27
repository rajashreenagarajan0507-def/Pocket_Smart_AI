from fastapi import APIRouter
from pydantic import BaseModel


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# Temporary in-memory user storage
users = {}


class RegisterRequest(BaseModel):
    username: str
    password: str


class LoginRequest(BaseModel):
    username: str
    password: str


@router.get("/")
def auth_home():
    return {
        "message": "PocketSmart AI Authentication is working!"
    }


@router.get("/health")
def auth_health():
    return {
        "status": "healthy"
    }


@router.post("/register")
def register(request: RegisterRequest):
    if request.username in users:
        return {
            "status": "error",
            "message": "Username already exists."
        }

    users[request.username] = request.password

    return {
        "status": "success",
        "message": "User registered successfully.",
        "username": request.username
    }


@router.post("/login")
def login(request: LoginRequest):
    if request.username not in users:
        return {
            "status": "error",
            "message": "User not found."
        }

    if users[request.username] != request.password:
        return {
            "status": "error",
            "message": "Incorrect password."
        }

    return {
        "status": "success",
        "message": "Login successful.",
        "username": request.username
    }


@router.post("/logout")
def logout():
    return {
        "status": "success",
        "message": "Logout successful."
    }