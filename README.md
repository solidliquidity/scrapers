# Sequel scrapers
This package provides structured classes to extract company data from their home website. It includes URLsoup for straightforward text and link extraction, as well as LLMScrape for leveraging language models with the use of SmartScraperGraph (information and further examples can be found here https://colab.research.google.com/drive/1sEZBonBMGP44CtO6GQTwAlL0BGJXjtfd?usp=sharing).

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

```
pip install -r requirements.txt
```

# Usage
```
# Option 1: scrape page without LLM.
urlsoup_instance = URLsoup(url)
df1 = urlsoup_instance.get_URLsoup_df()
URLsoup_df = pd.concat([URLsoup_df, df1], ignore_index=True)

# Option 2: scrape page with LLM. 
# input hugging face token
token = '****'
# choose model
model_name = 'EleutherAI/gpt-neox-20b' 
# choose prompt
prompt = f"Summarize the services offered by the company at {url} and list any founders' names mentioned."'
llm_scraper_instance = LLMscraper(model_name, token)
df2 = llm_scraper_instance.get_LLMscraper_df(url, prompt)
LLMscraper_df = pd.concat([LLMscraper_df, df2], ignore_index=True)
```

# How this can be improved

1. More models- build on option 2 to integrate OpenAI.

2. More sources- Linkedin, Crunchbase APIs to get founder background and growth metrics.

3. Clean the broad data capture from option 1. Identify keyworks, feed to LLM to derive insights.

# Further questions

## Why build https://www.pitchleague.ai?

Founders use pitchleague to get feedback improve their pitches. Competition score motivates founders to use the site more. This creates a greater network and more data for sequel to capture. 

## How to combine information from pitch decks and crawling websites?

Vector databases can be used, where data from pitch decks and websites is embedded. The claims in the pitch deck can be checked with the corresponding website data and monitored over time to see if their objectives are being met. More information from alternative data sources can be added too, to add to similarity searches and clustering. 