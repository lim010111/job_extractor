from bs4 import BeautifulSoup
from selenium import webdriver

def get_page_count(what, where=""):
    base_url = "https://kr.indeed.com/jobs?"
    browser = webdriver.Chrome()
    browser.get(
        f"{base_url}q={what}&l={where}"
    )
    soup = BeautifulSoup(browser.page_source, "html.parser")
    job_count_string = soup.find('div', class_="jobsearch-JobCountAndSortPane-jobCount").find('span').string
    
    # isdigit() -> ���ڿ����� ���ڸ� �����Ͽ� ����Ʈ�� ����
    job_count = []
    for string in job_count_string:
        if string.isdigit():
            job_count.append(string)
    
    # ������ �� 15���� ������ �����Ƿ� ������ / 15
    # ��, ������ �������� ���� �������� ���� ��� ������ ���� �ٸ��� ������ ���̽� �����ϱ�
    # type(job_count): list -> str -> int 
    job_count = int("".join(job_count))
    if job_count % 15 == 0:
        pages = job_count // 15
    else:
        pages = (job_count // 15) + 1
            
    return pages

def extract_indeed_jobs(what, where=""):
    results = [] 
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
                    'location': location.string,
                    'position': title.replace(",", " ")
                }
                results.append(job_data)
        
    return results