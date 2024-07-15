from scrapy.crawler import CrawlerProcess
from scrapers.linkedin_spider import LinkedinJobsSpider
from scrapers.jobie_spider import JobieJobsSpider

def run_linkedin_scraper():
    process = CrawlerProcess()
    process.crawl(LinkedinJobsSpider)
    process.start()

def run_jobie_scraper():
    process = CrawlerProcess()
    process.crawl(JobieJobsSpider)
    process.start()
