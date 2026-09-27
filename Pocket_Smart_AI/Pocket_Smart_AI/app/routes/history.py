from fastapi import APIRouter

router = APIRouter(
    prefix="/history",
    tags=["History"]
)

# Temporary history storage
history = {}


@router.get("/")
def history_home():
    return {
        "message": "PocketSmart AI History is working!"
    }


@router.get("/{username}")
def get_history(username: str):
    user_history = history.get(username, [])

    return {
        "status": "success",
        "username": username,
        "history": user_history
    }


@router.post("/{username}")
def add_history(
    username: str,
    planner: str,
    budget: float,
    description: str,
    recommendation: str
):
    if username not in history:
        history[username] = []

    history[username].append({
        "planner": planner,
        "budget": budget,
        "description": description,
        "recommendation": recommendation
    })

    return {
        "status": "success",
        "message": "Recommendation added to history.",
        "username": username
    }