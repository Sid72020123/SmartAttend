import os
import secrets
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Annotated

from dotenv import load_dotenv
from pydantic import ValidationError
from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from starlette.middleware.sessions import SessionMiddleware

from .database import Base, engine, get_db
from .models import create_tables, Organizer, Event
from .schemas import RegisterInput, LoginInput, OrganizerOut, EventCreate, EventOut
from .security import hash_password, verify_password

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


def utc_isoformat(value: datetime) -> str:
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    else:
        value = value.astimezone(timezone.utc)
    return value.isoformat().replace("+00:00", "Z")


def render_template(request: Request, template: str, **context):
    return templates.TemplateResponse(
        request=request,
        name=template,
        context={
            **context,
            "csrf_token": csrf_token(request),
        },
    )


def get_current_organizer(request: Request, db: Session):
    organizer_id = request.session.get("organizer_id")
    if not organizer_id:
        return None

    organizer = db.get(Organizer, organizer_id)
    return OrganizerOut(id=organizer.id, name=organizer.name, email=organizer.email)


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
            message=e.errors()[0]["msg"],
        )

    organizer = Organizer(
        name=form.name,
        email=form.email,
        password_hash=hash_password(form.password),
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


# Login
@app.get("/login")
def login(request: Request):
    if request.session.get("organizer_id"):
        return redirect("/dashboard")
    return render_template(request, "login.html")


@app.post("/login")
def login_user(
    request: Request,
    db: Annotated[Session, Depends(get_db)],
    email: Annotated[str, Form()],
    password: Annotated[str, Form()],
    csrf: Annotated[str, Form()],
):
    if not valid_csrf(request, csrf):
        return render_template(
            request,
            "login.html",
            error=True,
            message="Your form expired. Please try again.",
        )

    try:
        form = LoginInput(
            email=email,
            password=password,
        )
    except ValidationError as e:
        return render_template(
            request,
            "login.html",
            error=True,
            message=e.errors()[0]["msg"],
        )

    organizer = db.query(Organizer).filter(Organizer.email == form.email).first()

    if not organizer or not verify_password(form.password, organizer.password_hash):
        return render_template(
            request,
            "login.html",
            error=True,
            message="Invalid email or password.",
        )

    request.session.clear()
    request.session["organizer_id"] = organizer.id
    csrf_token(request)

    return redirect("/dashboard")


# Logout
@app.post("/logout")
def logout(
    request: Request,
    csrf: Annotated[str, Form()],
):
    if not valid_csrf(request, csrf):
        return redirect("/dashboard")

    request.session.clear()
    return redirect("/")


# Dashboard
@app.get("/dashboard")
def dashboard(
    request: Request,
    db: Annotated[Session, Depends(get_db)],
):

    organizer = get_current_organizer(request, db)
    if not organizer:
        return redirect("/login")

    raw_events = (
        db.query(Event)
        .filter(Event.organizer_id == organizer.id)
        .order_by(Event.created_at.desc())
        .all()
    )

    events = [
        EventOut(
            id=e.id,
            title=e.title,
            is_open=e.is_open,
            created_at=e.created_at,
            created_at_iso=utc_isoformat(e.created_at),
        )
        for e in raw_events
    ]

    return render_template(
        request, "dashboard.html", organizer=organizer, events=events
    )


# Create Event
@app.get("/events/create")
def create_event(
    request: Request,
    db: Annotated[Session, Depends(get_db)],
):
    if not get_current_organizer(request, db):
        return redirect("/login")

    return render_template(request, "create_event.html")


@app.post("/events/create")
def create_event_post(
    request: Request,
    db: Annotated[Session, Depends(get_db)],
    csrf: Annotated[str, Form()],
    title: Annotated[str, Form()],
):
    organizer = get_current_organizer(request, db)

    if not organizer:
        return redirect("/login")

    if not valid_csrf(request, csrf):
        return render_template(
            request,
            "create_event.html",
            error=True,
            message="Your form expired. Please try again.",
        )

    try:
        form = EventCreate(title=title)
    except ValidationError as e:
        return render_template(
            request,
            "create_event.html",
            error=True,
            message=e.errors()[0]["msg"],
        )

    new_event = Event(
        title=form.title,
        qr_token=secrets.token_urlsafe(32),
        organizer_id=organizer.id,
        is_open=True,
        created_at=datetime.now(timezone.utc).replace(tzinfo=None),
    )

    db.add(new_event)
    db.commit()
    db.refresh(new_event)

    # TODO: generate QR code and save it

    return redirect("/dashboard")
