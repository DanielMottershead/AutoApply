from DuunitoriScraper.data_models import *
from lxml import etree
from bs4 import BeautifulSoup
from datetime import date
import requests
import re

def get_salary_range(uri: str) -> SalaryRange:
    response = requests.get(uri)
    posting = BeautifulSoup(response.text, "html.parser")

    pay_range_text: str =posting.find_all("p", class_="header__info")[-1].get_text()
    pay_range_text =pay_range_text.replace(" ", "")

    if("–" in pay_range_text):
        pattern = r".*?(\d+)\s*–\s*(\d+)"
        match = re.search(pattern, pay_range_text, re.DOTALL)

        if match:
            first_salary = match.group(1)
            second_salary = match.group(2)
            return SalaryRange(int(first_salary), int(second_salary))
    else:
        pattern = r"(\d+)"
        match = re.search(pattern, pay_range_text, re.DOTALL)
        if match:
            return SalaryRange(int(match.group(1)), int(match.group(1)))
    
def scrape_postings(postings: list) -> list[JobPosting]:
    postings_to_return = []
    for posting in postings:
        link_elem = posting.find("a", class_="job-box__hover gtm-search-result")
        uri = link_elem["href"]
        posted = posting.find("span", class_="job-box__job-posted").get_text().split(" ")[1]

        if(len(posted) <= 6):
            posted = f"{posted}{date.today().year}"

        posting_data = JobPosting()
        posting_data.job_id = uri.split("-")[-1]
        posting_data.job_title = link_elem.get_text()
        posting_data.link = f"https://duunitori.fi{uri}"
        posting_data.posted = posted

        if(posting.find("span", class_="tag tag--salary tag--salary-icon") != None):
            posting_data.salary_range =get_salary_range(posting_data.link)

        postings_to_return.append(posting_data)

    return postings_to_return

def get_page_count(base_url: str) -> int:
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, "html.parser")
    return int(soup.find_all("a", class_="pagination__pagenum")[-1].text)