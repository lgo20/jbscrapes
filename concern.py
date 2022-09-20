import re
import scrapy
from scrapy.loader import ItemLoader
from idj.items import JobsItem

# scrapy crawl concern -O concern.json


class ConcernSpider(scrapy.Spider):

    name = "concern"
    start_urls = ["https://jobs.concern.net/jobs/vacancy/find/results/"]

    def parse(self, response):
        # get cookies, find pagestamp and get all jobs
        api_url = response.xpath(
            '//script[contains(., "_gridhandler")]/text()'
        ).re_first(r"var url = '(/[^']+_gridhandler[^']+)")
        if api_url:
            api_url = "https://jobs.concern.net" + api_url
            yield scrapy.Request(
                url=api_url,
                callback=self.parse_jobs,
            )

    def parse_jobs(self, response):
        for job_url in response.xpath(
            '//div[@class="ListGridContainer"]/div//a[contains(@href, "/description/")]/@href'
        ).getall():
            yield scrapy.Request(
                url=response.urljoin(job_url),
                callback=self.parse_job,
            )

        next_page = response.xpath(
            '//div[@class="pagingButtons"]/a[contains(@class, "scroller_movenext")][not(@disabled)]/@href'
        ).get()
        if next_page:
            yield scrapy.Request(
                url=response.urljoin(next_page),
                callback=self.parse_jobs,
            )

    def parse_job(self, response):
        l = ItemLoader(item=JobsItem(), response=response)
        l.add_value("id", response.url, re=r"(\d+)/description/")
        l.add_value("url", response.url)
        l.add_xpath("title", "//h1/text()", re=r"(.+?)\s+\(")

        application_url = response.xpath('//a[.="Apply Now"]/@href').get()
        if application_url:
            l.add_value("application_url", response.urljoin(application_url))

        # l.add_xpath('date_created', '') # TODO
        l.add_xpath(
            "date_closing", '//div[.="Closing Date:"]/following-sibling::div[1]/text()'
        )
        l.add_xpath("description", '//div[@class="earcu_posdescription"]')
        # l.add_xpath('category', '') # TODO
        l.add_xpath("location", '//div[.="Location:"]/following-sibling::div[1]/text()')
        l.add_xpath(
            "contract_type",
            '//div[.="Contract Type:"]/following-sibling::div[1]/text()',
        )
        l.add_xpath("salary", '//div[.="Salary:"]/following-sibling::div[1]/text()')
        l.add_value("organisation", "Concern Worldwide")
        l.add_value("website", "https://www.concern.net/")
        l.add_value("wp_org_id", 5317)

        item = l.load_item()
        yield item
