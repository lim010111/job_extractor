from bs4 import BeautifulSoup
from selenium import webdriver

def get_page_count(what, where=""):
    base_url = "https://kr.indeed.com/jobs?"
    browser = webdriver.Chrome()
    browser.get(
        f"{base_url}q={what}&l={where}"
    )
    soup = BeautifulSoup(browser.page_source, "html.parser")
    pagination = soup.find('nav', role="navigation")
    pages = pagination.find_all('div', class_="css-tvvxwd ecydgvn1")
    count = len(pages)
    if count >= 5:
        return 5
    elif count == 0:
        return 1
    else:
        return count-1

def extract_indeed_jobs(what, where=""):
    results = [] # 반복문 안에 있을 경우 새로운 루프를 돌 때 마다 empty list 가 되기 때문에 반복문 밖으로 빼주기
    pages = get_page_count(what, where="")
    print("Found", pages, "pages")
    for page in range(pages):
        base_url = "https://kr.indeed.com/jobs?"
        final_url = f"{base_url}q={what}&l={where}&start={page*10}"
        print("Requesting=> ", final_url)
        browser = webdriver.Chrome()
        browser.get(final_url)
        
        soup = BeautifulSoup(browser.page_source, "html.parser")
        
        job_list = soup.find('ul', class_="jobsearch-ResultsList")
        jobs = job_list.find_all('li', recursive=False)
        for job in jobs:
            zone = job.find('div', class_="mosaic-zone")
            if zone == None:
                anchor = job.select_one("h2 a")
                title = anchor['aria-label']
                link = anchor['href']
                company = job.find('span', class_="companyName")
                location = job.find('div', class_="companyLocation")

                job_data = {
                    'link': f"kr.indeed.com{link}",
                    'company': company.string.replace(",", " "),
                    'location': location.string.replace(",", " "),
                    'position': title.replace(",", " ")
                }
                results.append(job_data)
        
    return results