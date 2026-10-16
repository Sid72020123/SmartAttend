import os
import secrets
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Annotated

from dotenv import load_dotenv
from pydantic import ValidationError
from fastapi import FastAPI, Request, Form, Depends
from fastapi.exceptions import RequestValidationError
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from starlette.middleware.sessions import SessionMiddleware

from .database import Base, engine, get_db
from .models import create_tables, Organizer
from .schemas import RegisterInput
from .security import hash_password

# --- Config ---
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

SESSION_SECRET = os.getenv("SESSION_SECRET")
if not SESSION_SECRET:
    raise RuntimeError("SESSION_SECRET must be configured")


# --- FastAPI Application Setup ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield


app = FastAPI(title="SmartAttend", lifespan=lifespan)

app.add_middleware(
    SessionMiddleware,
    secret_key=SESSION_SECRET,
    session_cookie="smartattend_session",
    max_age=60 * 60 * 8,
    same_site="lax",
    https_only=os.getenv("COOKIE_SECURE", "false").lower() == "true",
)

app.mount(
    "/static",
    StaticFiles(directory=str(BASE_DIR / "static")),
    name="static",
)

# --- Helper Methods ---


def redirect(path: str):
    return RedirectResponse(path, status_code=303)


def csrf_token(request: Request) -> str:
    if "csrf_token" not in request.session:
        request.session["csrf_token"] = secrets.token_urlsafe(32)
    return request.session["csrf_token"]


def valid_csrf(request: Request, submitted: str) -> bool:
    expected = request.session.get("csrf_token", "")
    return bool(expected) and secrets.compare_digest(expected, submitted)


def render_template(request: Request, template: str, **context):
    return templates.TemplateResponse(
        request=request,
        name=template,
        context={
            **context,
            "csrf_token": csrf_token(request),
        },
    )


# --- App Routes ---


# Health
@app.get("/health")
def health():
    return {"health": "ok", "status": "running"}


# Root
@app.get("/")
def home(request: Request):
    return render_template(request, "index.html")


# Register
@app.get("/register")
def register(request: Request):
    if request.session.get("organizer_id"):
        return redirect("/dashboard")
    return render_template(request, "register.html")


@app.post("/register")
def register_user(
    request: Request,
    db: Annotated[Session, Depends(get_db)],
    name: Annotated[str, Form()],
    email: Annotated[str, Form()],
    password: Annotated[str, Form()],
    confirm_password: Annotated[str, Form()],
    csrf: Annotated[str, Form()],
):
    if not valid_csrf(request, csrf):
        return render_template(
            request,
            "register.html",
            error=True,
            message="Your form expired. Please try again.",
        )

    try:
        form = RegisterInput(
            name=name,
            email=email,
            password=password,
            confirm_password=confirm_password,
        )
    except ValidationError as e:
        return render_template(
            request,
            "register.html",
            error=True,
            messages=e.errors()[0]["msg"],
        )

    organizer = Organizer(
        name=form.name,
        email=form.email,
        password_hash=hash_password(password),
    )
    db.add(organizer)

    try:
        db.commit()
        db.refresh(organizer)
    except IntegrityError:
        db.rollback()
        return render_template(
            request,
            "register.html",
            error=True,
            message="An account with that email already exists.",
        )

    request.session.clear()
    request.session["organizer_id"] = organizer.id
    csrf_token(request)

    return redirect("/dashboard")


@app.get("/test")
def test_route(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            # "title": "Home",
        },
    )
