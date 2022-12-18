import datetime
import logging
from dataclasses import dataclass
import azure.functions as func
import requests
from bs4 import BeautifulSoup
from datetime import date
from lxml import etree

@dataclass
class SalaryRange:
    lower_bound: int
    upper_bound: int

    def get_average_salary(self) -> int:
        return (self.lower_bound + self.upper_bound) / 2

@dataclass
class JobPosting:
    job_id: str = ''
    job_title: str = ''
    posted: str = None
    salary_range: SalaryRange = None
    link: str = ''


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


def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()
    final_list_of_postings = []
    base_url = "https://duunitori.fi/tyopaikat?filter_salary=1&haku=Ohjelmointi%20ja%20ohjelmistokehitys%20(ala)"#"https://duunitori.fi/tyopaikat?haku=software%20engineer"

    try:
        response = requests.get(base_url)
        soup = BeautifulSoup(response.text, "html.parser")
        pages_count = int(soup.find_all("a", class_="pagination__pagenum")[-1].text)
        for i in range(1, pages_count + 1):
            response = requests.get(f"{base_url}&sivu={i}")
            soup = BeautifulSoup(response.text, "html.parser")
            postings_container = soup.find("div", class_="grid-sandbox grid-sandbox--tight-bottom grid-sandbox--tight-top")
            postings = postings_container.find_all("div", class_="grid grid--middle job-box job-box--lg")

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
                    
                
                final_list_of_postings.append(posting_data)
    except Exception as e:
                logging.critical(f"Exception: {e.with_traceback}")





