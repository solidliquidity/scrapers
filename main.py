import logging
from scrapers import URLsoup, LLMscraper
import pandas as pd

# websites to scrape
websites = [
    "https://tonestro.com/",
    "https://www.sendtrumpet.com/",
    "https://www.prewave.com/",
    "https://twinn.health/",
    "https://kokoon.io/"
]

# configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s')


def main():

    # input model
    model_name = 'EleutherAI/gpt-neox-20b'

    URLsoup_df = pd.DataFrame()
    LLMscraper_df = pd.DataFrame()

    for url in websites:
        logging.info(f"Processing {url}...")

        # input prompt
        prompt = f"Summarize the services offered by the company at {url} and list any founders' names mentioned."

        # 1: scrape page without LLMs and create dataframe
        urlsoup_instance = URLsoup(url)
        df1 = urlsoup_instance.get_URLsoup_df(url)
        URLsoup_df = pd.concat([URLsoup_df, df1], ignore_index=True)

        # 2: scrape page with LLM and create dataframe
        # input hugging face token (https://huggingface.co/)
        token = '****'
        llm_scraper_instance = LLMscraper(model_name, token)
        df2 = llm_scraper_instance.get_LLMscraper_df(url, prompt)
        LLMscraper_df = pd.concat([LLMscraper_df, df2], ignore_index=True)

        logging.info(f"Processed {url} successfully.")

    # display dataframes
    logging.info("URLsoup DataFrame:")
    logging.info(URLsoup_df)
    logging.info("LLMscraper DataFrame:")
    logging.info(LLMscraper_df)


if __name__ == "__main__":
    main()
