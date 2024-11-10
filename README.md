# Sequel scrapers
Purpose: This script gathers company information from websites, extracting product details, founders’ names, and uses an LLM to generate insights.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

# Installation

pip install -r requirements.txt

# Usage

1. URLsoup extracts data from a webpage taking the homepage's URL as a single argument without the use of LLMs. Functions allow you to get all links, get all text data for a given link, and extract all names within that text.

2. LLMscrape uses SmartScraperGraph. More information and further examples can be found here: https://colab.research.google.com/drive/1sEZBonBMGP44CtO6GQTwAlL0BGJXjtfd?usp=sharing. The model can be parsed into LLMscaper. The below is taken from main.py.

scraper = URLsoup(url)
text = scraper.get_text()
links = scraper.get_links()

print(f"Extracted text:\n{text[:500]}...\n")  # Show a snippet of text
print(f"Extracted links: {links}\n")

model_name = 'gpt-neox'  # Choose model
llm_scraper = LLMscraper(model_name)
response = llm_scraper.generate_response(
    f"Summarize the services offered by the company at {url} and list any founders' names mentioned."
)

print(f"LLM Response:\n{response}\n")