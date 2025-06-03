
# app/main.py
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles # Not strictly needed for this version, but good for future CSS/JS
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
import os

# Adjust imports if your project structure is different or if files are not in a package.
# Assuming 'app' is a package and these modules are within it.
from .interfaces import PodcastItemDTO, FeedDataProvider, PostFormatter
from .feed_processing import SpreakerFeedParser
from .social_media_formatters import WhatsappFacebookFormatter

# Global variables for services - initialized during lifespan
feed_provider: FeedDataProvider
post_formatter: PostFormatter

# Configuration
FEED_URL = "https://www.spreaker.com/show/6622205/episodes/feed"

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Context manager to initialize resources on startup and clean up on shutdown.
    Initializes the feed provider and post formatter.
    """
    global feed_provider, post_formatter
    feed_provider = SpreakerFeedParser(feed_url=FEED_URL)
    post_formatter = WhatsappFacebookFormatter() # Default formatter
    print("FastAPI application startup: Services initialized.")
    yield
    # Clean up services on shutdown (if needed)
    print("FastAPI application shutdown.")

app = FastAPI(lifespan=lifespan, title="Podcast Post Generator", version="1.0.0")

# Determine the base directory of the current file (main.py)
# This is to correctly locate templates and static files if any.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Mount static files (e.g., for CSS, JS) if you have them in a 'static' directory
# Example: app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

# Initialize Jinja2Templates to render HTML
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

@app.get("/", response_class=HTMLResponse, summary="Generar Post para Redes Sociales",
         description="Obtiene un episodio aleatorio del podcast y genera un post para redes sociales.")
async def get_social_post_page(request: Request):
    """
    Endpoint principal que:
    1. Obtiene todos los episodios del feed.
    2. Selecciona un episodio aleatorio.
    3. Formatea la información del episodio para un post de red social.
    4. Renderiza una página HTML con el post generado.
    """
    try:
        all_items = await feed_provider.get_all_items()
        if not all_items:
            # If no items are found, render the page with an error message
            return templates.TemplateResponse("index.html", {
                "request": request,
                "post_title": "Error",
                "formatted_post": "No se pudieron obtener episodios del podcast. Intenta recargar.",
                "image_url": None,
                "episode_link": None,
                "error_message": "No se encontraron episodios en el feed."
            })

        selected_item = feed_provider.select_random_item(all_items)
        if not selected_item:
             # This case should ideally not be hit if all_items is not empty and select_random_item works
            return templates.TemplateResponse("index.html", {
                "request": request,
                "post_title": "Error",
                "formatted_post": "No se pudo seleccionar un episodio.",
                "image_url": None,
                "episode_link": None,
                "error_message": "No se pudo seleccionar un episodio aleatorio."
            })

        # Generate the social media post text using the formatter
        formatted_post_text = post_formatter.format_post(selected_item)
        
        # The image_url is part of selected_item, pass it to the template
        image_to_display = selected_item.image_url
        # Provide a direct link to listen to the episode
        episode_listen_link = selected_item.audio_url if selected_item.audio_url else selected_item.link

        return templates.TemplateResponse("index.html", {
            "request": request,
            "post_title": selected_item.title,
            "formatted_post": formatted_post_text,
            "image_url": image_to_display,
            "episode_link": episode_listen_link,
            "error_message": None # No error
        })
    except HTTPException as http_exc: # Catch HTTPExceptions specifically if raised by dependencies
        print(f"HTTP Exception occurred: {http_exc.detail}")
        return templates.TemplateResponse("index.html", {
            "request": request,
            "post_title": "Error",
            "formatted_post": f"Ocurrió un error HTTP: {http_exc.detail}. Por favor, intenta de nuevo.",
            "image_url": None,
            "episode_link": None,
            "error_message": str(http_exc.detail)
        })
    except Exception as e:
        # Log the exception for debugging purposes
        print(f"An unexpected error occurred: {e}")
        # Render an error page or return an error response
        # For a user-facing page, it's better to show a friendly error in the template
        return templates.TemplateResponse("index.html", {
            "request": request,
            "post_title": "Error",
            "formatted_post": "Ocurrió un error inesperado al generar el post. Por favor, intenta de nuevo.",
            "image_url": None,
            "episode_link": None,
            "error_message": "Error interno del servidor. " + str(e) # Avoid showing raw error to user in prod
        })

# To run this application (assuming this file is in 'app/main.py'):
# From the directory containing the 'app' folder, run:
# uvicorn app.main:app --reload --port 8001
