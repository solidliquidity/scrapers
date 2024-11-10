import pandas as pd
import requests
from typing import List, Optional, Dict
from transformers import AutoTokenizer, AutoModelForCausalLM
import logging
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from base_classes import BaseScraper, BaseLLMScraper
import spacy

logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s')


class URLsoup(BaseScraper):
    """Concrete implementation of BaseScraper for web scraping without LLM."""

    def __init__(self, main_url: str):
        super().__init__(main_url)
        # Initialize all attributes to None
        self._soup: Optional[BeautifulSoup] = None
        self._links: Optional[List[str]] = None
        self._text: Optional[str] = None
        self._names: Optional[List[str]] = None
        # Then populate attributes
        self._initialize_soup()
        self._initialize_links()
        self._initialize_text()
        self._initialize_names()

    def _initialize_soup(self):
        """Fetch and parse HTML from the URL."""
        try:
            response = requests.get(self.main_url)
            response.raise_for_status()
            self._soup = BeautifulSoup(response.text, 'html.parser')
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to retrieve the page: {e}")

    def _initialize_links(self):
        """Extract all unique links from the parsed HTML."""
        self._links = []
        if self._soup:
            for link in self._soup.find_all('a', href=True):
                full_url = urljoin(self.main_url, link['href'])
                if full_url not in self._links:
                    self._links.append(full_url)

    def _initialize_text(self):
        """Extract all text content from the parsed HTML."""
        if self._soup:
            self._text = self._soup.get_text(separator="\n").strip()
        else:
            self._text = 'No text available'

    def _initialize_names(self):
        """Get all names from text using spaCy."""
        if self._text:
            nlp = spacy.load("en_core_web_sm")
            doc = nlp(self._text)
            self._names = [
                ent.text for ent in doc.ents if ent.label_ == "PERSON"]
        else:
            self._names = []

    def get_soup(self) -> Optional[BeautifulSoup]:
        return self._soup

    def get_links(self) -> List[str]:
        return self._links

    def get_text(self) -> str:
        return self._text

    def get_names(self) -> List[str]:
        return self._names

    def get_URLsoup_df(self, url: str) -> pd.DataFrame:
        """Generate a DataFrame containing urls, texts, names."""
        main_soup = URLsoup(url)
        main_links = main_soup.get_links()
        data = {'url': [], 'texts': [], 'names': []}
        URLsoup_df = pd.DataFrame()
        for link in main_links:
            link_soup = URLsoup(link)
            data['url'] = link
            data['texts'] = link_soup.get_text()
            data['names'] = link_soup.get_names()
            df1 = pd.DataFrame(data)
            URLsoup_df = pd.concat([URLsoup_df, df1], ignore_index=True)
        return URLsoup_df


class LLMscraper(BaseLLMScraper):
    """Implementation of BaseLLMScraper for Hugging Face models."""

    def __init__(self, model_name: str, token: str):
        super().__init__(model_name, token)
        self._tokenizer = AutoTokenizer.from_pretrained(
            model_name, token=token)
        self._model = self.create_model(model_name)

    def create_model(self, model_name: str):
        """Load a causal language model."""
        try:
            model = AutoModelForCausalLM.from_pretrained(
                model_name, token=self.token)
            return model
        except Exception as e:
            raise ValueError(f"Failed to load model '{model_name}': {e}")

    def generate_response(self, prompt: str, max_length: int = 1024) -> str:
        """Generate a response using the loaded model."""
        inputs = self._tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=max_length
        )
        outputs = self._model.generate(**inputs, max_new_tokens=150)
        return self._tokenizer.decode(outputs[0], skip_special_tokens=True)

    def create_graph_config(self) -> Dict:
        """Generate configuration details for a SmartScraperGraph."""
        return {
            "llm": {
                "model": self._model,
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
