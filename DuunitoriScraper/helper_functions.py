from DuunitoriScraper.data_models import *
from bs4 import BeautifulSoup
from datetime import date
import datetime
import requests
import re

def get_company_info(posting: BeautifulSoup) -> str:
    try:
        info_block = posting.find_all("div", class_="1/1 1/3--desk grid__cell")[0]
        name = info_block.find_all("h2")[0].get_text()
        return name
    except:
        return "Company name not automatically found"

def get_description(posting: BeautifulSoup) -> str:
    try:
        return posting.find("div", class_="gtm-apply-clicks description description--jobentry").get_text()
    except:
        return "No description automatically found"
    

def get_salary_range(posting: BeautifulSoup) -> SalaryRange:
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
            date_string  = f"{posted}{date.today().year}"
            potential_date =  datetime.datetime.strptime(date_string, '%d.%m.%Y')
            if potential_date <= datetime.datetime.today():
                posted = date_string
            else:
                posted = f"{posted}{date.today().year-1}"

        posting_data = JobPosting()
        posting_data.job_id = uri.split("-")[-1]
        posting_data.job_title = link_elem.get_text()
        posting_data.link = f"https://duunitori.fi{uri}"
        posting_data.posted = posted

        #if the posting contains saley info, currently always true
        if(posting.find("span", class_="tag tag--salary tag--salary-icon") != None):
            response = requests.get(posting_data.link)
            posting = BeautifulSoup(response.text, "html.parser")

            salary_range = get_salary_range(posting)
            posting_data.salary_range_low = salary_range.lower_bound
            posting_data.salary_range_high = salary_range.upper_bound
            
            posting_data.company = get_company_info(posting)
            posting_data.description = get_description(posting)

        postings_to_return.append(posting_data)

    return postings_to_return

def get_page_count(base_url: str) -> int:
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, "html.parser")
    page_count_elem = soup.find_all("a", class_="pagination__pagenum")
    if(page_count_elem != None and len(page_count_elem) > 1):
        return int(soup.find_all("a", class_="pagination__pagenum")[-1].text)
    else:
        return 1