from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from pymongo import MongoClient

# Set up MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['linkedin_jobs']
collection = db['job_postings']

# Set up Chrome WebDriver options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized")  # Maximize the browser window

# Initialize Chrome WebDriver with options
driver = webdriver.Chrome(options=chrome_options)

# Navigate to LinkedIn and log in
driver.get('https://www.linkedin.com/')
# Add code to automate the login process here

# Navigate to the job search page
driver.get('https://www.linkedin.com/jobs/')

try:
    # Wait for the search box to be visible
    search_box = WebDriverWait(driver, 40).until(EC.visibility_of_element_located((By.CLASS_NAME, 'jobs-search-box__text-input')))
except TimeoutException as ex:
    print("TimeoutException: Failed to find the search box within the specified time.")
    driver.quit()
    exit()
except NoSuchElementException as ex:
    print("NoSuchElementException: Failed to locate the search box element.")
    driver.quit()
    exit()

# Search for jobs (e.g., software engineer jobs)
search_box.send_keys('Software Engineer')
#search_box.submit()

# Scrape job postings (only the first 5)
try:
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'jobs-search-results__list-item')))
    job_cards = driver.find_elements(By.CLASS_NAME, 'jobs-search-results__list-item')[:5]  # Only first 5 job cards
    for card in job_cards:
        try:
            title_element = card.find_element(By.TAG_NAME, 'h3')
            company_element = card.find_element(By.CLASS_NAME, 'job-card-container__company-name')
            
            # Retrieve text content
            title = title_element.text
            company = company_element.text
            
            # Insert data into MongoDB
            job_data = {'title': title, 'company': company}
            collection.insert_one(job_data)
            
        except StaleElementReferenceException:
            # Handle StaleElementReferenceException by re-finding the elements
            title_element = card.find_element(By.TAG_NAME, 'h3')
            company_element = card.find_element(By.CLASS_NAME, 'job-card-container__company-name')
            
            # Retrieve text content
            title = title_element.text
            company = company_element.text
            
            # Insert data into MongoDB
            job_data = {'title': title, 'company': company}
            collection.insert_one(job_data)

except TimeoutException:
    print("TimeoutException: Failed to load job search results.")
finally:
    # Close the WebDriver
    driver.quit()
