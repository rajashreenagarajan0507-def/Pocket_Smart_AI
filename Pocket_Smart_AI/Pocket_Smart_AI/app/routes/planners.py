from fastapi import APIRouter
from pydantic import BaseModel

from app.services.gemini_service import generate_recommendation


router = APIRouter(
    prefix="/planners",
    tags=["Planners"]
)


class PlannerRequest(BaseModel):
    budget: float
    description: str = ""


@router.get("/")
def planners_home():
    return {
        "message": "PocketSmart AI Planners are working!"
    }


@router.get("/health")
def planners_health():
    return {
        "status": "healthy"
    }


@router.post("/home")
def generate_home(request: PlannerRequest):
    prompt = f"""
You are PocketSmart AI, a smart budget assistant.

Create a practical home budget recommendation.

Budget: ₹{request.budget}
Requirement: {request.description}

Give:
1. Suggested allocation
2. Important items to prioritize
3. Ways to save money

Keep the answer clear and practical.
"""

    recommendation = generate_recommendation(prompt)

    return {
        "planner": "Home",
        "budget": request.budget,
        "description": request.description,
        "recommendation": recommendation
    }


@router.post("/party")
def generate_party(request: PlannerRequest):
    prompt = f"""
You are PocketSmart AI, a smart budget assistant.

Create a practical party budget recommendation.

Budget: ₹{request.budget}
Party details: {request.description}

Give:
1. Food and drinks allocation
2. Decoration allocation
3. Other important expenses
4. Money-saving suggestions

Keep the answer clear and practical.
"""

    recommendation = generate_recommendation(prompt)

    return {
        "planner": "Party",
        "budget": request.budget,
        "description": request.description,
        "recommendation": recommendation
    }


@router.post("/jewelry")
def generate_jewelry(request: PlannerRequest):
    prompt = f"""
You are PocketSmart AI, a smart budget assistant.

Create a practical jewelry purchase recommendation.

Budget: ₹{request.budget}
Requirement: {request.description}

Give:
1. Suggested spending range
2. Suitable options to consider
3. Tips for staying within budget

Do not make claims about current gold prices unless they are provided.
Keep the answer clear and practical.
"""

    recommendation = generate_recommendation(prompt)

    return {
        "planner": "Jewelry",
        "budget": request.budget,
        "description": request.description,
        "recommendation": recommendation
    }