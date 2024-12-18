# scrapers
This package provides structured classes to extract company data from their home website. It includes URLsoup for regular text and link extraction, as well as LLMScrape for leveraging large language models with the use of SmartScraperGraph (details and further examples can be found here: https://colab.research.google.com/drive/1sEZBonBMGP44CtO6GQTwAlL0BGJXjtfd?usp=sharing).

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
  - [URLsoup](#urlsoup)
  - [LLMScrape](#llmscrape)

# Installation

```
pip install -r requirements.txt
```

# Usage
```
from scrapers import URLsoup, LLMscraper

# Option 1: scrape page without LLM.
# input url
url = 'example.com'
urlsoup_instance = URLsoup(url)
df1 = urlsoup_instance.get_URLsoup_df()
URLsoup_df = pd.concat([URLsoup_df, df1], ignore_index=True)

# Option 2: scrape page with LLM. 
# input hugging face token (https://huggingface.co/)
token = '****'
# input model
model_name = 'EleutherAI/gpt-neox-20b' 
# input prompt
prompt = f"Summarize the services offered by the company at {url} and list any founders' names mentioned."'
llm_scraper_instance = LLMscraper(model_name, token)
df2 = llm_scraper_instance.get_LLMscraper_df(url, prompt)
LLMscraper_df = pd.concat([LLMscraper_df, df2], ignore_index=True)
```
