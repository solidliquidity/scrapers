from abc import ABC, abstractmethod
from typing import List, Optional
import logging
from abc import ABC, abstractmethod
from typing import Dict
from bs4 import BeautifulSoup


class BaseScraper(ABC):
    """Abstract base class for all scrapers."""

    def __init__(self, main_url: str):
        self.main_url = main_url

    @abstractmethod
    def get_soup(self) -> Optional[BeautifulSoup]:
        """Retrieve and parse the main webpage."""
        pass

    @abstractmethod
    def get_links(self) -> List[str]:
        """Retrieve all links from the page."""
        pass

    @abstractmethod
    def get_text(self) -> str:
        """Retrieve all text content from the page."""
        pass


class BaseLLMScraper(ABC):
    """Abstract base class for language model scrapers."""

    def __init__(self, model_name: str):
        self.model_name = model_name
        self.model = self.create_model(model_name)

    @abstractmethod
    def create_model(self, model_name: str):
        """Create and initialize the model."""
        pass

    @abstractmethod
    def generate_response(self, prompt: str, max_length: int = 1024) -> str:
        """Generate a response from the language model based on a prompt."""
        pass

    @abstractmethod
    def create_graph_config(self) -> Dict:
        """Create configuration for graph generation."""
        pass
