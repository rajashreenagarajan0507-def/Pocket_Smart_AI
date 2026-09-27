from fastapi import APIRouter, HTTPException
from app.models.schemas import UserCreate, UserLogin, UserResponse

router = APIRouter()

# Temporary in-memory database
users = []

next_user_id = 1


@router.post("/register", response_model=UserResponse)
def register(user: UserCreate):
    global next_user_id

    # Check if email already exists
    for existing_user in users:
        if existing_user["email"].lower() == user.email.lower():
            raise HTTPException(
                status_code=400,
                detail="Email already registered"
            )

    new_user = {
        "id": next_user_id,
        "name": user.name,
        "email": user.email,
        "password": user.password
    }

    users.append(new_user)
    next_user_id += 1

    return {
        "id": new_user["id"],
        "name": new_user["name"],
        "email": new_user["email"]
    }


@router.post("/login")
def login(user: UserLogin):
    for existing_user in users:
        if (
            existing_user["email"].lower() == user.email.lower()
            and existing_user["password"] == user.password
        ):
            return {
                "success": True,
                "message": "Login successful",
                "user": {
                    "id": existing_user["id"],
                    "name": existing_user["name"],
                    "email": existing_user["email"]
                }
            }

    raise HTTPException(
        status_code=401,
        detail="Invalid email or password"
    )


@router.get("/users")
def get_users():
    return [
        {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"]
        }
        for user in users
    ]