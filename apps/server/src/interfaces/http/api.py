from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager
from sqlmodel import SQLModel
from src.infrastructure.database import engine
from src.utils.env import get_env_var
from .posts import router as posts_router
from .users import router as users_router
from .audiences import router as audiences_router
from .media_items import router as media_items_router
from .auth import router as auth_router
from .frontend import router as frontend_router

# Import all models to ensure they're included in metadata
from src.domain.models.post import Post
from src.domain.models.user import User
from src.domain.models.audience import Audience
from src.domain.models.media_item import MediaItem
from src.domain.models.links.audience_user_link import AudienceUserLink
from src.domain.models.links.post_audience_link import PostAudienceLink

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

# Add CORS middleware
allowed_origins = [get_env_var("FRONTEND_URL")]
# Add www variant if main domain doesn't start with www
frontend_url = get_env_var("FRONTEND_URL")
if not frontend_url.startswith("https://www.") and "localhost" not in frontend_url:
    www_variant = frontend_url.replace("https://", "https://www.")
    allowed_origins.append(www_variant)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(posts_router)
app.include_router(users_router)
app.include_router(audiences_router)
app.include_router(media_items_router)
app.include_router(auth_router)
app.include_router(frontend_router)

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <!DOCTYPE html>
    <html>
      <head><meta charset="utf-8"><title>Life Abroad</title></head>
      <body>
        <h1>It works </h1>
        <p>FastAPI single-page app running in Docker.</p>
      </body>
    </html>
    """
