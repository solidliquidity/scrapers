import pandas as pd
import requests
from typing import List, Optional, Dict
from transformers import AutoTokenizer, AutoModelForCausalLM, GPTNeoXForCausalLM
import logging
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from base_classes import BaseScraper, BaseLLMScraper
import spacy

logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s')


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

    def get_names(self):
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(self.text)
        names = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]

        return names

    def get_URLsoup_df(url: str) -> pd.DataFrame:
        main_soup = URLsoup(url)
        main_links = main_soup.get_links()
        data = {'url': [], 'names': [], 'texts': []}

        for link in main_links:
            link_soup = URLsoup(link)
            data['url'].append(link)
            data['texts'].append(link_soup.get_text())
            data['names'].append(link_soup.get_names())

        URLsoup_df = pd.DataFrame(data)
        return URLsoup_df


class LLMscraper(BaseLLMScraper):
    """Implementation of BaseLLMScraper for Hugging Face models."""

    def __init__(self, model_name: str, token: str):
        super().__init__(model_name, token)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, token=self.token)
        self.model = self.create_model(model_name)

    def create_model(self, model_name: str):
        """Load a causal language model."""
        try:
            # Explicitly pass the token to access private models
            model = AutoModelForCausalLM.from_pretrained(model_name, use_auth_token=self.token)
            return model
        except Exception as e:
            raise ValueError(f"Failed to load model '{model_name}': {e}")

    def generate_response(self, prompt: str, max_length: int = 1024) -> str:
        """Generate a response using the loaded model."""
        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=max_length
        )
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

    def get_LLMscraper_df(self, url: str, prompt: str) -> pd.DataFrame:
        """Generate a DataFrame containing the model's response for the provided URL."""
        response = self.generate_response(prompt)
        data = {'url': [url], 'response': [response]}
        LLMscraper_df = pd.DataFrame(data)
        return LLMscraper_df
