from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
import math
from django.http import JsonResponse

def get_jobs(request):
    headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"}
    url='https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Python%20%28Programming%20Language%29&location=Las%20Vegas%2C%20Nevada%2C%20United%20States&geoId=100293800&currentJobId=3415227738&start={}'
    job_ids = []
    job_details = {}
    all_jobs = []

    for i in range(0, 1):
        res = requests.get(url.format(i), headers=headers)
        soup = BeautifulSoup(res.text,'html.parser')
        all_jobs_on_page = soup.find_all("li")

        for x in range(0,len(all_jobs_on_page)):
            jobid = all_jobs_on_page[x].find("div",{"class":"base-card"}).get('data-entity-urn').split(":")[3]
            job_ids.append(jobid)

    target_url='https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{}'
    print(job_ids)

    for j in range(0, len(job_ids)):
        res = requests.get(target_url.format(job_ids[j]), headers=headers)
        soup = BeautifulSoup(res.text,'html.parser')

        try:
            job_details["company"] = soup.find("div",{"class":"top-card-layout__card"}).find("a").find("img").get('alt')
        except:
            job_details["company"] = None

        try:
            job_details["job-title"] = soup.find("div",{"class":"top-card-layout__entity-info"}).find("a").text.strip()
        except:
            job_details["job-title"] = None

        try:
            job_details["level"] = soup.find("ul",{"class":"description__job-criteria-list"}).find("li").text.replace("Seniority level","").strip()
        except:
            job_details["level"] = None

        try:
            job_details["description"] = soup.find("div", {"class": "description__text"}).text.strip()
        except:
            job_details["description"] = None
        
        all_jobs.append(job_details)
        job_details={}

    return JsonResponse({'jobs': all_jobs}, status=200)

