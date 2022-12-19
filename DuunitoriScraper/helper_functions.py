from DuunitoriScraper.data_models import *
from lxml import etree
from bs4 import BeautifulSoup
from datetime import date
import requests

def get_salary_range(uri: str) -> SalaryRange:
    response = requests.get(uri)
    posting = BeautifulSoup(response.text, "html.parser")
    dom = etree.HTML(str(posting))
    pay_range_text: str = dom.xpath('/html/body/div[6]/div/div[1]/div[1]/div[1]/div[3]/p[3]/text()')[1]

    no_new_lines = pay_range_text.replace("\n", "")
    no_spaces = no_new_lines.replace(" ", "")
    pay_range = no_spaces.replace("€/kk", "")

    if not('–' in pay_range):
        return SalaryRange(int(pay_range), int(pay_range))
    else:
        splitted = pay_range.split('–')
        return SalaryRange(int(splitted[0]), int(splitted[1]))
    
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