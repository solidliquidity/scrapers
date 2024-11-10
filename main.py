import logging
from scrapers import URLsoup, LLMscraper

# Sample test websites
websites = [
    "https://tonestro.com/",
    "https://www.sendtrumpet.com/",
    "https://www.prewave.com/",
    "https://twinn.health/",
    "https://kokoon.io/"
]

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    for url in websites:
        logging.info(f"Processing {url}...")

        # Step 1: Scrape the page
        scraper = URLsoup(url)
        text = scraper.get_text()
        links = scraper.get_links()

        logging.info(f"Extracted text:\n{text[:500]}...")  # Show a snippet of text
        logging.info(f"Extracted links: {links}")

        # Step 2: Use LLM to analyze text
        model_name = 'gpt-neox'  # Choose model
        llm_scraper = LLMscraper(model_name)
        response = llm_scraper.generate_response(
            f"Summarize the services offered by the company at {url} and list any founders' names mentioned."
        )

        logging.info(f"LLM Response:\n{response}\n")

if __name__ == "__main__":
    main()
