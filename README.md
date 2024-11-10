# Sequel scrapers
Purpose: This script gathers company information from websites, extracting product details, founders’ names, and uses an LLM to generate insights.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
  - [URLsoup](#urlsoup)
  - [LLMScrape](#llmscrape)
- [Improvements](#improvements)
- [Further Questions](#further-questions)
  - [Why Build PitchLeague.ai?](#why-build-pitchleagueai)
  - [Combining Information from Pitch Decks and Crawling Websites](#combining-information-from-pitch-decks-and-crawling-websites)
- [Contributing](#contributing)
- [License](#license)


# Installation

pip install -r requirements.txt

# Usage
'''
1. URLsoup extracts data from a webpage taking the homepage's URL as a single argument without the use of LLMs. Functions allow you to get all links, get all text data for a given link, and extract all names within that text.

2. LLMscrape uses SmartScraperGraph. More information and further examples can be found here

https://colab.research.google.com/drive/1sEZBonBMGP44CtO6GQTwAlL0BGJXjtfd?usp=sharing. 

The model can be parsed into LLMscaper. The below is taken from main.py.

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
'''
# How this can be improved

Additional Data Sources:
Integrate the LinkedIn or Crunchbase API to supplement the data on founders and growth metrics. LinkedIn can confirm founder names, and Crunchbase can provide investment rounds or growth rates.

Open Graph Metadata Extraction:
Many websites have metadata that describes the business, product, or team. Using a simple Open Graph parser could help pull additional structured information, especially for newer startups.
Growth Metrics:

Implement keyword scanning or LLM analysis to search for mentions of funding rounds, partnerships, or new product launches. These indicators suggest the startup’s growth potential.

# Further questions

## why build https://www.pitchleague.ai?

Competition motivates founders to use the site more. This creates a wider user base and provides Sequel with more data to use. 

## how can we combine information from pitch decks and crawling websites?