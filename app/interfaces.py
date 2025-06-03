# app/interfaces.py
from abc import ABC, abstractmethod
from typing import List, Optional
import random

from pydantic import BaseModel, HttpUrl # HttpUrl for URL validation

class PodcastItemDTO(BaseModel):
    """
    Data Transfer Object for a podcast episode.
    Uses Pydantic for data validation and serialization.
    """
    title: str
    link: HttpUrl # Link to the episode page
    audio_url: Optional[HttpUrl] = None # Direct link to the audio file
    image_url: Optional[HttpUrl] = None # Link to the episode image
    description: Optional[str] = None   # Episode summary/description
    published_date: Optional[str] = None # Publication date as string

    class Config:
        # Pydantic V2: an_instance.model_dump()
        # Pydantic V1: an_instance.dict()
        # For compatibility, you can check Pydantic version or stick to one.
        # This example assumes Pydantic V2 features might be used elsewhere,
        # but basic functionality is similar.
        # For older Pydantic:
        # orm_mode = True (if creating from ORM objects)
        pass


class FeedDataProvider(ABC):
    """
    Abstract Base Class defining the interface for a feed data provider.
    This allows for different feed sources or parsing strategies in the future.
    """
    @abstractmethod
    async def get_all_items(self) -> List[PodcastItemDTO]:
        """Fetches and parses all items from the feed."""
        pass

    def select_random_item(self, items: List[PodcastItemDTO]) -> Optional[PodcastItemDTO]:
        """Selects a random item from a list of podcast items."""
        if not items:
            return None
        return random.choice(items)


class PostFormatter(ABC):
    """
    Abstract Base Class defining the interface for a post formatter.
    This allows for different formatting strategies for various social media platforms.
    """
    @abstractmethod
    def format_post(self, item: PodcastItemDTO) -> str:
        """Formats the podcast item data into a string suitable for a social media post."""
        pass
