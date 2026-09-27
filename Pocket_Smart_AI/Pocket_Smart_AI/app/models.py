from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List


# ============================================================
# USER MODELS
# ============================================================

class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr


# ============================================================
# BASIC BUDGET MODEL
# ============================================================

class BudgetRequest(BaseModel):
    income: float = Field(..., ge=0)
    expenses: float = Field(..., ge=0)
    savings_goal: float = Field(default=0, ge=0)


# ============================================================
# GENERAL RECOMMENDATION MODEL
# ============================================================

class RecommendationRequest(BaseModel):
    income: float = Field(..., ge=0)
    expenses: float = Field(..., ge=0)
    category: Optional[str] = None


# ============================================================
# HOME PLANNER
# ============================================================

class HomeItem(BaseModel):
    name: str
    quantity: int = Field(default=1, ge=1)


class HomeRecommendationRequest(BaseModel):
    budget: float = Field(..., gt=0)
    room_type: str = Field(..., min_length=2)
    style: Optional[str] = None
    items: List[HomeItem] = Field(default_factory=list)


# ============================================================
# PARTY PLANNER
# ============================================================

class PartyRecommendationRequest(BaseModel):
    budget: float = Field(..., gt=0)
    guests: int = Field(..., ge=1)
    event_type: str = Field(..., min_length=2)
    venue: Optional[str] = None
    food_preference: Optional[str] = None
    decoration_style: Optional[str] = None


# ============================================================
# JEWELRY PLANNER
# ============================================================

class JewelryRecommendationRequest(BaseModel):
    budget: float = Field(..., gt=0)
    occasion: str = Field(..., min_length=2)
    style: Optional[str] = None
    metal_preference: Optional[str] = None
    outfit_color: Optional[str] = None


# ============================================================
# AI RECOMMENDATION RESPONSE
# ============================================================

class ProductRecommendation(BaseModel):
    name: str
    category: str
    platform: str
    price: float
    description: str
    link: Optional[str] = None


class RecommendationResponse(BaseModel):
    title: str
    summary: str
    budget: float
    estimated_total: float
    recommendations: List[ProductRecommendation]