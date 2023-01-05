import datetime
import logging
import azure.functions as func
import requests
from bs4 import BeautifulSoup
import os
import json
# from helper_functions import *
from DuunitoriScraper.helper_functions import *

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()
    final_list_of_postings = []
    base_url = "https://duunitori.fi/tyopaikat?filter_salary=1&haku=Ohjelmointi%20ja%20ohjelmistokehitys%20(ala)"#"https://duunitori.fi/tyopaikat?haku=software%20engineer"

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
    current_directory = os.getcwd()

    # Create the full path of the file
    file_name = "posts2.json"
    file_path = os.path.join(current_directory, file_name)

    # Create the file
    file = open(file_path, "w")

    # Write the string to the file
    #body = body.replace("\u200b", "")
    json_string = json.dumps(final_list_of_postings, default=lambda x: x.__dict__)
    file.write(json_string)

    # Close the file
    file.close()





