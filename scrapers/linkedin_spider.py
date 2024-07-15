import scrapy
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient
from scrapy.crawler import CrawlerProcess
from selenium.common.exceptions import TimeoutException

class LinkedinJobsSpider(scrapy.Spider):
    name = 'linkedin_jobs'
    start_urls = ['https://www.linkedin.com/login']

    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['job_matching']
        self.job_postings = self.db['job_postings']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.login, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"})

    def login(self, response):
        self.logger.info("Logging in...")
        driver = webdriver.Chrome()
        driver.get(response.url)
        try:
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'username')))
        except TimeoutException:
            self.logger.error("Username input field not found within the specified time.")

        # Input username and password
        driver.find_element_by_id('username').send_keys('erkan48592@hotmail.com')
        driver.find_element_by_id('password').send_keys('your_password')

        # Click login button
        driver.find_element_by_css_selector('button[type="submit"]').click()

        try:
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//ul[contains(@class, "jobs-search__results-list")]')))
        except TimeoutException:
            self.logger.error("Element not found within the specified time.")

        # Handle cookie consent alert
        try:
            cookie_alert = driver.find_element_by_xpath('//div[@id="KIE_CONSENT"]')
            accept_button = cookie_alert.find_element_by_xpath('.//button[@action-type="ACCEPT"]')
            accept_button.click()
        except Exception as e:
            self.logger.error("Cookie consent alert not found or could not be dismissed:", e)

        sel = Selector(text=driver.page_source)
        job_listings = sel.xpath('//li[contains(@class, "jobs-search__result-item")]')[:10]  # Limit to the first 10 listings
        self.logger.info("Job listings found: %s", len(job_listings))
        for job in job_listings:
            title = job.xpath('.//h3/a/text()').get()
            company = job.xpath('.//h4/a/text()').get()
            location = job.xpath('.//span[contains(@class, "job-result-card__location")]/text()').get()
            description = job.xpath('.//p[contains(@class, "job-result-card__snippet")]/text()').get()
            url = job.xpath('.//a[contains(@class, "result-card__full-card-link")]/@href').get()

            job_data = {
                'title': title,
                'company': company,
                'location': location,
                'description': description,
                'url': url
            }

            self.job_postings.insert_one(job_data)

        driver.quit()

    def closed(self, reason):
        self.client.close()

# Run the scraper
if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(LinkedinJobsSpider)
    process.start()
