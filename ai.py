import re
import scrapy
from scrapy.loader import ItemLoader
from idj.items import JobsItem
import dateparser

# scrapy crawl a-- -O output/a--.json


class A-Spider(scrapy.Spider):

    name = "a--"

    # custom_settings = {"FEEDS": {"%(name)s.json": {"format": "json"}}}

    start_urls = ["https://xxx"]

    def parse(self, response):
        # get cookies, find pagestamp and get all jobs
        api_url = response.xpath(
            '//script[contains(., "_gridhandler")]/text()'
        ).re_first(r"var url = '(/[^']+_gridhandler[^']+)")
        if api_url:
            api_url = "https://xxx" + api_url
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

    def parse_job(self, response):
        l = ItemLoader(item=JobsItem(), response=response)
        l.add_value("id", response.url, re=r"(\d+)/description/")
        l.add_value("url", response.url)
        l.add_xpath("title", "//h1/text()", re=r"(.+?)\s+\(")

        application_url = response.xpath('//a[.="Apply for this role"]/@href').get()
        if application_url:
            l.add_value("application_url", response.urljoin(application_url))

        # l.add_xpath('date_created', '') # TODO
        # l.add_xpath(
        #     "date_closing", '//div[.="Closing Date:"]/following-sibling::div[1]/text()'
        # )

        l.add_value(
            "date_closing",
            dateparser.parse(
                response.xpath(
                    '//div[.="Closing Date:"]/following-sibling::div[1]/text()',
                ).get(),
                date_formats=["D Month YYYY"],
            ),
        )

        l.add_xpath("description", '//div[@class="earcu_posdescription"]')
        # l.add_xpath('category', '') # TODO
        l.add_xpath("location", '//div[.="Location:"]/following-sibling::div[1]/text()')
        # l.add_xpath('contract_type', '') # TODO
        # l.add_xpath('salary', '') # TODO
        l.add_value("organisation", "xxx")
        l.add_value("website", "xxx")

        l.add_value("contract_type_jboard", None)
        

        l.add_value("employer_id_jboard", 167337)

        item = l.load_item()
        yield item
