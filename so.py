from soup import get_soup
from bs4 import BeautifulSoup
import requests


#마지막 페이지 숫자 구하기
def get_last_page(url):
    soup = get_soup(url)
    
    pagination = soup.find("div", {"class": "s-pagination"})
    if pagination is not None:
      pages = pagination.find_all("a")
      last_page = (pages[-2].find("span")).string
    else:
      last_page = 1

    return int(last_page)


#각 박스(그리드)의 정보를 추출하여 return
def extract_info(grid):
    title = grid.find("h2").a["title"]  #구직글 제목

    company, location = grid.find(
        "h3",
        {  #회사, 장소
            "class": "fc-black-700"
        }).find_all(
            "span", recursive=False)

    company = company.get_text(strip=True)

    location = location.string.strip()

    job_id = grid["data-jobid"]
    link = f"https://stackoverflow.com/jobs?id={job_id}"

    return {
        "title": title,
        "company": company,
        "location": location,
        "link": link
    }


#첫 페이지부터 마지막 페이지까지 모든 일자리 정보 추출
def extract_jobs(url, last_page_num):
    job_infos = []

    for page_num in range(last_page_num):
        Nth_url = f"{url}&pg={page_num+1}"
        Nth_page_soup = get_soup(Nth_url)

        job_info_boxes = Nth_page_soup.find_all("div", {"class": "-job"})
        for job_info_box in job_info_boxes:
          job_info = extract_info(job_info_box)
          job_infos.append(job_info)

    return job_infos


#입력한 검색어를 통한 일자리 추출
def search_jobs(keyword):
    url = f"https://stackoverflow.com/jobs?q={keyword}"

    last_page_num = get_last_page(url)
    jobs = extract_jobs(url, last_page_num)

    return jobs
