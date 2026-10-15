from contextlib import asynccontextmanager
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from .models import create_tables

# --- Config ---
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


# --- FastAPI Application Setup ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield


app = FastAPI(title="SmartAttend", lifespan=lifespan)

app.mount(
    "/static",
    StaticFiles(directory=str(BASE_DIR / "static")),
    name="static",
)


@app.get("/health")
def health():
    return {"health": "ok", "status": "running"}


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            # "title": "Home",
        },
    )


@app.get("/login")
def login(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
    )


@app.get("/test")
def test_route(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            # "title": "Home",
        },
    )
