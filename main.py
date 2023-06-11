"""
Main script for scraping Naver Cafe
"""


import os
from dotenv import load_dotenv
from utils.scraper import NaverCafeScraper

if __name__ == "__main__":
    load_dotenv()

    cafe_url = os.getenv("CAFE_URL")

    scraper = NaverCafeScraper(url=os.getenv("CAFE_URL"))

    scraper.scrape_author(author_name=os.getenv("AUTHOR"))
