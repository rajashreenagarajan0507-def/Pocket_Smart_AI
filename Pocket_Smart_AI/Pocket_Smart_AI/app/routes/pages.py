from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter(
    tags=["Pages"]
)

templates = Jinja2Templates(
    directory="app/templates"
)


@router.get("/")
def welcome_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="welcome.html"
    )


@router.get("/planners")
def planners_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="planners.html"
    )


@router.get("/home-planner")
def home_planner(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="home.html"
    )


@router.get("/party-planner")
def party_planner(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="party.html"
    )


@router.get("/jewelry-planner")
def jewelry_planner(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="jewelry.html"
    )


@router.get("/health")
def pages_health():
    return {
        "status": "healthy"
    }