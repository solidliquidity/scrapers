from abc import ABC, abstractmethod
from typing import List, Optional, Dict
from bs4 import BeautifulSoup
import pandas as pd


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

    @abstractmethod
    def get_names(self) -> List[str]:
        """Retrieve all names (persons) from the text content."""
        pass

    @abstractmethod
    def get_URLsoup_df(self) -> pd.DataFrame:
        """Generate a DataFrame containing links, names, and texts from the main URL."""
        pass


class BaseLLMScraper(ABC):
    """Abstract base class for language model scrapers."""

    def __init__(self, model_name: str, token: str):
        self.model_name = model_name
        self.token = token
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

    @abstractmethod
    def get_LLMscraper_df(self, url: str) -> pd.DataFrame:
        """Generate a DataFrame containing the model's response for the provided URL."""
        pass
