from bs4 import BeautifulSoup
import requests
import pymongo

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["linkedin_jobs"]
collection = db["software_developer"]

# Scrape LinkedIn job page
url = "https://www.linkedin.com/jobs/software-developer-jobs"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Filter and save the first 5 jobs
jobs = soup.find_all("div", class_="job-card-container")
software_developer_jobs = []
for job in jobs:
    title = job.find("span", class_="screen-reader-text").text.strip()
    description = job.find("p", class_="job-card-description").text.strip()
    if "software" in title.lower() or "software" in description.lower():
        software_developer_jobs.append({"title": title, "description": description})
    if len(software_developer_jobs) >= 5:
        break

# Save to MongoDB
for job in software_developer_jobs:
    collection.insert_one(job)

print("Jobs saved to MongoDB")
