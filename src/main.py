import os
import secrets
from contextlib import asynccontextmanager
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from starlette.middleware.sessions import SessionMiddleware

from .models import create_tables

# --- Config ---
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

SESSION_SECRET = os.getenv("SESSION_SECRET", "")


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


@app.get("/test")
def test_route(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            # "title": "Home",
        },
    )
