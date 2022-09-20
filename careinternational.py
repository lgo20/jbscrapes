from typing import Dict, Final
import scrapy
import w3lib.html
from scrapy.loader import ItemLoader
from idj.items import JobsItem

# TODO capture item info across two pages

# python -m scrapy shell https://www.careinternational.org.uk/jobs/current-vacancies
# python -m scrapy shell https://www.careinternational.org.uk/node/523618
# scrapy shell https://ce0169li.webitrent.com/ce0169li_webrecruitment/wrd/run/ETREC107GF.open?VACANCY_ID=6949292oBX&WVID=949155007A&LANG=USA
# scrapy crawl careinternational -O output/careinternational.json
# python -m scrapy crawl careinternational -O output/careinternational.json


class CareInternationalSpider(scrapy.Spider):
    name: Final = "careinternational"
    allowed_domains = ["careinternational.com", "careinternational.org.uk", "webitrent.com"]
    start_urls = ["https://www.careinternational.org.uk/jobs/current-vacancies"]

    def parse(self, response):
        job_content = response.css("div.view-content")
        for job_url in job_content.xpath('//div/article/footer/ul/li/a/@href').getall():
            link = response.urljoin(job_url)
            yield scrapy.Request(link, self.parse_job)

    # def parse_job(self, response):
    #     # get link to ATS job posting
    #     link = response.xpath('//*[@id="main"]/div/a[text()="Apply now"]/@href').get()
    #     yield scrapy.Request(link, self.parse_ats_job)

    # def get_dl(self, response):
    #     dl = response.css("div.job-profile-details.newStyle")
    #     dt_list = dl.css("dt")
    #     dl_obj = dict()
    #     for dt in dt_list:
    #         dt_value = dt.css("::text").get()
    #         dd_value = dt.xpath("./following-sibling::dd/text()").get()
    #         dl_obj[dt_value] = dd_value
    #     return dl_obj

    def parse_job(self, response):
        l = ItemLoader(item=JobsItem(), selector=response.css("div.content.ppb"))

        # job = response.css("div.content.ppb")
        # dt_list = dl.css("dt::text").extract()
        # dd_list = dl.css("dd::text").extract()
        # dl_list = zip(dt_list, dd_list)

        # dl2 = CareInternationalSpider.get_dl(self, response)

        # dl_obj = dict()
        # dt_list = dl.css("dt")
        # for dt in dt_list:
        #     dt_value = dt.css("::text").get()
        #     dd_value = dt.xpath("./following-sibling::dd/text()").get()
        #     dl_obj[dt_value] = dd_value

        l.add_css("title", "div.job-description > div.header > h2::text")
        #main > div > div.info > div:nth-child(4) > div
        l.add_css("id", 'div.info > div:nth-child(4) > div::text') 
        l.add_css("application_url", "a.apply-link::attr(href)")
        l.add_value("url", response.url)
        l.add_css("contract_type", "span.work-type::text")
        l.add_css("category", "span.categories::text")
        l.add_css("date_created", "span.open-date > time::attr(datetime)")
        l.add_css("date_closing", "span.close-date > time::attr(datetime)")
        l.add_css("description", "div[id='job-details']")

        l.add_value("website", "https://www.careinternational.org.uk/")
        l.add_value("wp_org_id", 5169)

        # item["decription"] = w3lib.html.remove_tags(
        #     decription, which_ones=('<div id="job-details">')
        # )
        yield l.load_item()
Footer
© 2022 GitHub, Inc.
Footer navigation
Terms
