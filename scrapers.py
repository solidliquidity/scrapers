from typing import List, Optional, Dict
from transformers import AutoTokenizer, AutoModelForCausalLM, GPTNeoXForCausalLM
import logging
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
from base_classes import BaseScraper, BaseLLMScraper

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

class URLsoup(BaseScraper):
    """Concrete implementation of BaseScraper for web scraping."""

    def __init__(self, main_url: str):
        super().__init__(main_url)
        self._soup: Optional[BeautifulSoup] = None
        self._links: Optional[List[str]] = None
        self._text: Optional[str] = None

    def get_soup(self) -> Optional[BeautifulSoup]:
        """Fetch and parse HTML from the URL."""
        try:
            response = requests.get(self.main_url)
            response.raise_for_status()
            self._soup = BeautifulSoup(response.text, 'html.parser')
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to retrieve the page: {e}")
        return self._soup

    def get_links(self) -> List[str]:
        """Extract all unique links from the parsed HTML."""
        if self._links is None:
            self._links = []
            if self._soup:
                for link in self._soup.find_all('a', href=True):
                    full_url = urljoin(self.main_url, link['href'])
                    if full_url not in self._links:
                        self._links.append(full_url)
        return self._links

    def get_text(self) -> str:
        """Extract all text content from the parsed HTML."""
        if self._text is None and self._soup:
            self._text = self._soup.get_text(separator="\n").strip()
        return self._text or 'No text available'

## add another for OpenAI
class LLMscraper(BaseLLMScraper):
    """Implementation of BaseLLMScraper for Hugging Face models."""

    def __init__(self, model_name: str):
        super().__init__(model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = self.create_model(model_name)

    def create_model(self, model_name: str, use_gpu: bool = True, precision: str = "half"):
        """Load a causal language model with optional GPU and precision settings."""
        try:
            model = AutoModelForCausalLM.from_pretrained(model_name)
            if use_gpu and torch.cuda.is_available():
                if precision == "half":
                    model = model.half().cuda()
                elif precision == "float":
                    model = model.cuda()
            return model
        except Exception as e:
            raise ValueError(f"Failed to load model '{model_name}': {e}")

    def generate_response(self, prompt: str, max_length: int = 1024) -> str:
        """Generate a response using the loaded model."""
        inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=max_length)
        outputs = self.model.generate(**inputs, max_new_tokens=150)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

    def create_graph_config(self) -> Dict:
        """Generate configuration details for a SmartScraperGraph."""
        return {
            "llm": {
                "model": self.model,
                "temperature": 0,
                "format": "json",
            },
            "verbose": True,
            "headless": True
        }
