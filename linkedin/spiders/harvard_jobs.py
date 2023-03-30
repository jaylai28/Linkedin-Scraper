import scrapy
import re

class LinkedJobsSpider(scrapy.Spider):
    name = "linkedin_jobs"
    api_url = 'https://academicpositions.harvard.edu/postings/search' 
    

    def start_requests(self):
        first_job_on_page = 0
        first_url = self.api_url + str(first_job_on_page)
        yield scrapy.Request(url=first_url, callback=self.parse_job)


    def parse_job(self, response):
        home_url = 'https://academicpositions.harvard.edu'
        job_item = {}
        tag_list = []

        for url in response.css('a::attr(href)'):
            if re.search('postings\/[0-9]', url):
                a = home_url + '/postings/' + url
                tag_list.append(a)
        

        for posting_url in tag_list:
            if response.css('tr').extract() != []:
                for field in response.css('tr td::text'):
                    job_item[field] = field
                yield scrapy.Request(url=posting_url, callback=self.parse_job)



        
        # if crawl_next(new_url):
        #     new_url = home_url + make_requests(new_url).find(class_='next_page').get("href")
        #     next_url = self.api_url + str(first_job_on_page)
        #     yield scrapy.Request(url=next_url, callback=self.parse_job)

