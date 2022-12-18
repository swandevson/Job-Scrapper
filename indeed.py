from soup import get_soup
from bs4 import BeautifulSoup
import requests


def get_last_page(url):
    soup = get_soup(url)
    #print(soup)
    pagination = soup.find("div", {"class": "pagination"})
    if pagination is not None:
      pages = pagination.find_all("a")
      last_page = pages[-2].string
    else:
      last_page = 1
    
    return int(last_page)


def extract_info(grid):
    title = grid.find("h2").a["title"]
    
    company = grid.find("span", {"class": "company"})
    if company is None:
      print("No Attribute!")
      return

    if company.a is None:
        company_name = str(company.string)
    else:
        company_name = str(company.a.string)
    company_name = company_name.strip("\n")

    location = grid.find("div", {"class": "recJobLoc"})["data-rc-loc"]

    job_id = grid["data-jk"]

    return {
        'title':
        title,
        'company':
        company_name,
        'location':
        location,
        'link':
        f"https://kr.indeed.com/%EC%B1%84%EC%9A%A9%EB%B3%B4%EA%B8%B0?jk={job_id}"
    }


def extract_jobs(url, last_page_num=1, limit=10):
    job_infos = []

    for page_num in range(last_page_num):
        Nth_url = f"{url}&start={page_num*limit}"
        Nth_page_soup = get_soup(Nth_url)

        job_info_boxes = Nth_page_soup.find_all(
            "div", {"class": "jobsearch-SerpJobCard"})
        for job_info_box in job_info_boxes:
            if not job_info_box:
              return job_infos
            job_info = extract_info(job_info_box)
            job_infos.append(job_info)

    return job_infos


def search_jobs(keyword):
    limit = 50
    url = f"https://kr.indeed.com/jobs?q={keyword}&limit={limit}"

    last_page_num = get_last_page(url)

    jobs = extract_jobs(url, last_page_num, limit)

    return jobs
