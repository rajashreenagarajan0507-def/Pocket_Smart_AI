from fastapi import APIRouter

router = APIRouter(
    prefix="/session",
    tags=["Session"]
)

# Temporary session storage
sessions = {}


@router.get("/")
def session_home():
    return {
        "message": "PocketSmart AI Session is working!"
    }


@router.get("/health")
def session_health():
    return {
        "status": "healthy"
    }


@router.post("/start/{username}")
def start_session(username: str):
    sessions[username] = {
        "username": username,
        "logged_in": True
    }

    return {
        "status": "success",
        "message": "Session started.",
        "session": sessions[username]
    }


@router.get("/{username}")
def get_session(username: str):
    if username not in sessions:
        return {
            "status": "error",
            "message": "No active session."
        }

    return {
        "status": "success",
        "session": sessions[username]
    }


@router.post("/end/{username}")
def end_session(username: str):
    if username in sessions:
        sessions[username]["logged_in"] = False

    return {
        "status": "success",
        "message": "Session ended."
    }