import datetime
import logging
import azure.functions as func
import requests
from bs4 import BeautifulSoup
import os
import json

from DuunitoriScraper.helper_functions import *
from DuunitoriScraper.storage_service import *

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()
    final_list_of_postings = []
    base_url = "https://duunitori.fi/tyopaikat?filter_salary=1&haku=Ohjelmointi%20ja%20ohjelmistokehitys%20(ala)"

    try:
        pages_count = get_page_count(base_url)

        for i in range(1, pages_count + 1):
            response = requests.get(f"{base_url}&sivu={i}")
            soup = BeautifulSoup(response.text, "html.parser")
            postings_container = soup.find("div", class_="grid-sandbox grid-sandbox--tight-bottom grid-sandbox--tight-top")
            postings = postings_container.find_all("div", class_="grid grid--middle job-box job-box--lg")

            final_list_of_postings += scrape_postings(postings)
    except Exception as e:
                logging.critical(f"Exception: {e}")
    store_postings(final_list_of_postings)