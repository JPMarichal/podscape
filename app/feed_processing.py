# app/feed_processing.py
import feedparser # For parsing RSS/Atom feeds
import httpx      # For making asynchronous HTTP requests
from typing import List, Optional
import logging # For logging potential issues

# Assuming interfaces.py is in the same package directory
from .interfaces import FeedDataProvider, PodcastItemDTO

# Configure basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SpreakerFeedParser(FeedDataProvider):
    """
    A concrete implementation of FeedDataProvider for parsing Spreaker RSS feeds.
    """
    def __init__(self, feed_url: str):
        self.feed_url = feed_url

    async def get_all_items(self) -> List[PodcastItemDTO]:
        """
        Fetches the feed content asynchronously, parses it, and extracts podcast items.
        Returns a list of PodcastItemDTO objects.
        """
        items: List[PodcastItemDTO] = []
        try:
            async with httpx.AsyncClient(timeout=15.0) as client: # Increased timeout
                logger.info(f"Fetching feed from: {self.feed_url}")
                response = await client.get(self.feed_url)
                response.raise_for_status() # Raise an HTTPStatusError for bad responses (4xx or 5xx)
                feed_content = response.text
            
            # feedparser is synchronous, so it's called after awaiting the content
            parsed_feed = feedparser.parse(feed_content)

            if parsed_feed.bozo:
                # Bozo bit is 1 if the feed is not well-formed XML or has other issues
                logger.warning(f"Feed may be ill-formed. Bozo reason: {parsed_feed.bozo_exception}")

            if not parsed_feed.entries:
                logger.warning(f"No entries found in the feed from {self.feed_url}")
                return []

            logger.info(f"Found {len(parsed_feed.entries)} entries in the feed.")

            for entry in parsed_feed.entries:
                audio_url_str: Optional[str] = None
                if hasattr(entry, 'enclosures') and entry.enclosures:
                    for enc in entry.enclosures:
                        if enc.get('type', '').startswith('audio'):
                            audio_url_str = enc.href
                            break # Take the first audio enclosure
                
                image_url_str: Optional[str] = None
                # Try 'itunes_image' first (often a dict {'href': 'url'})
                itunes_image_obj = entry.get('itunes_image')
                if itunes_image_obj and isinstance(itunes_image_obj, dict):
                    image_url_str = itunes_image_obj.get('href')
                
                # Fallback to entry.image (often an object with a 'href' attribute)
                if not image_url_str and hasattr(entry, 'image') and hasattr(entry.image, 'href'):
                    image_url_str = entry.image.href
                
                # Fallback for media:thumbnail or other common image tags
                if not image_url_str and entry.get('media_thumbnail'):
                    # media_thumbnail is usually a list of dicts
                    if isinstance(entry.media_thumbnail, list) and entry.media_thumbnail:
                        image_url_str = entry.media_thumbnail[0].get('url')

                # Ensure URLs are valid or None before passing to Pydantic
                valid_link = entry.link if entry.link else None
                valid_audio_url = audio_url_str if audio_url_str else None
                valid_image_url = image_url_str if image_url_str else None
                
                # Description can be in 'summary' or 'description'
                description_text = entry.get('summary', entry.get('description', ''))

                try:
                    item = PodcastItemDTO(
                        title=entry.title or "Sin título",
                        link=valid_link or "http://example.com/invalid", # Provide a fallback or handle error
                        audio_url=valid_audio_url,
                        image_url=valid_image_url,
                        description=description_text,
                        published_date=entry.get('published')
                    )
                    items.append(item)
                except Exception as pydantic_exc: # Catch Pydantic validation errors specifically
                    logger.error(f"Pydantic validation error for entry '{entry.title}': {pydantic_exc}. Skipping item.")
                    logger.debug(f"Data causing Pydantic error: link='{valid_link}', audio='{valid_audio_url}', image='{valid_image_url}'")


        except httpx.RequestError as e:
            logger.error(f"HTTP request error fetching feed from {self.feed_url}: {e}")
            # Optionally, re-raise as a custom exception or handle as per application needs
            # For this app, returning an empty list and letting the endpoint handle it.
            return []
        except Exception as e:
            logger.error(f"An unexpected error occurred during feed processing: {e}", exc_info=True)
            return []
        
        return items
