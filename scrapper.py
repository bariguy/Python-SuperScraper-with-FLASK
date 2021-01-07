import requests 
from bs4 import BeautifulSoup
from save import save_to_file


# EXTRACT PAGES
def extract_pages(url):
    link = requests.get(url)
    indeed_soup = BeautifulSoup(link.text, "html.parser") #get html of the link
    class_pagination = indeed_soup.find("div", {"class":"pagination"}) #find the html with name div and class pagination
    pages = class_pagination.find_all("a") #find all objects that start with a 
    page = [] 
    for i in pages[:-1]:
        page.append(int(i.find("span").string)) #append the empty list with the name of span --> page numbers
    max_page = page[-1]
    return max_page #returns number of pages


def extract_jobs_and_companies(html):
        job_title = html.find("h2", {"class": "title"}).find("a")["title"]
        company = html.find("span", {"class":"company"})
        location = html.find("div",{"class":"recJobLoc"})["data-rc-loc"]
        job_id = html["data-jk"]
        company_anchor = company.find("a")
        if company_anchor is not None:
            company_title = (company_anchor.string)
        else:
            company_title = (company.string)
        
        return {"title": job_title, 
                "company": company_title,
                "location": location, 
                "link":f"https://www.indeed.com/viewjob?jk={job_id}"
                }

def extract_indeed_jobs(last_page, url):
        jobs = []
        for page in range(last_page):
            print(f"Scraping for: page{1+page}")
            page_url = url+"&start="+str(page*50)
            page_request = requests.get(page_url)
            job_soup = BeautifulSoup(page_request.text, "html.parser")
            each_job_html = job_soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
            for each in each_job_html:
                job = extract_jobs_and_companies(each) 
                jobs.append(job)  
        return jobs  


def get_jobs(word):
    url = f"https://www.indeed.com/jobs?q={word}&limit=50"
    pages = extract_pages(url)
    indeed_jobs = extract_indeed_jobs(pages, url)
    return indeed_jobs
