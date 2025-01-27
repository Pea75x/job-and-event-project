from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from django.http import JsonResponse
from .flashtext_helper import extract_skills
from .tech_skills_list import skills_list
from .general_skills_list import general_skills_list
import json

def get_skills(request):
    file_path = 'jobs/job_data.json'

    with open(file_path, 'r') as file:
        data = json.load(file)
        description = data["jobs"][1]["description"]
    
    skills = extract_skills(description, skills_list)
    general_skills = extract_skills(description, general_skills_list)

    return JsonResponse({'jobs': general_skills}, status=200)



def get_jobs(request):
    language = request.GET.get('language')
    headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"}
    job_ids = []
    job_details = {}
    all_jobs = []

    # get job ids
    url=f'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={language}&geoId=90009496&currentJobId=3415227738&start=0'

    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text,'html.parser')
    all_jobs_on_page = soup.find_all("li")

    for x in range(0,len(all_jobs_on_page)):
        jobid = all_jobs_on_page[x].find("div",{"class":"base-card"}).get('data-entity-urn').split(":")[3]
        job_ids.append(jobid)

    # get job details
    target_url='https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{}'

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
            job_description = soup.find("div", {"class": "description__text"}).text.strip()
            job_details["technical_skills"] = extract_skills(job_description, skills_list)
            job_details["general_skills"] = extract_skills(job_description, general_skills_list)
        except:
            job_details["technical_skills"] = None
            job_details["general_skills"] = None

        try:
            job_details["link"] = f"https://www.linkedin.com/jobs/view/{job_ids[j]}/"
        except:
            job_details["link"] = None
    
        all_jobs.append(job_details)
        job_details={}

    return JsonResponse({'jobs': all_jobs}, status=200)
