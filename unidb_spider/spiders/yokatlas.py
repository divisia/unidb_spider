from scrapy.selector.unified import Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import Spider, Request
from scrapy_splash import SplashRequest
from selenium.webdriver import Firefox, FirefoxOptions, FirefoxProfile
import time


class YOKAtlasCrawler(CrawlSpider):
    name = 'yokatlas'
    allowed_domains = ['yokatlas.yok.gov.tr']
    start_urls = ['https://yokatlas.yok.gov.tr/lisans-anasayfa.php']
    rules = (Rule(LinkExtractor(), callback="parse_item"),)
    driver = Firefox()


    def parse_item(self, response):
        vals = response.css('#univ2 option')
        for v in vals: 
            code = v.xpath("@value").get()
            name = v.css("::text").get()
            yield Request(f"https://yokatlas.yok.gov.tr/lisans-univ.php?u={code}", callback=self.parse_uni, meta={"code": code, "name": name})
    

    def parse_uni(self, response):
        panels = response.css(".panel.panel-primary")
        for panel in panels:
            major = panel.css(".panel-title div::text").get()
            subtl = panel.css(".panel-title div::text").get()
            deprt = panel.css("button::text").get()
            faclt = panel.css("font::text").get()
            link = panel.css("a::attr(href)").get()
            yield Request(f"https://yokatlas.yok.gov.tr/{link}", callback=self.parse_major, meta={"code": response.meta["code"], "name": response.meta["name"], "year": 2020, "major": major, "deprt": deprt, "faclt": faclt, "subtl": subtl})
            yield Request(f"https://yokatlas.yok.gov.tr/2019/{link}", callback=self.parse_major, meta={"code": response.meta["code"], "name": response.meta["name"], "year": 2019, "major": major, "deprt": deprt, "faclt": faclt, "subtl": subtl})
            yield Request(f"https://yokatlas.yok.gov.tr/2018/{link}", callback=self.parse_major, meta={"code": response.meta["code"], "name": response.meta["name"], "year": 2018, "major": major, "deprt": deprt, "faclt": faclt, "subtl": subtl})


    def parse_major(self, response):
        self.driver.get(response.url)
        btn = self.driver.find_element_by_css_selector('.openall')
        btn.click()
        time.sleep(3)
        sel = Selector(text=self.driver.page_source)
        major_extra = sel.css("h2.panel-title.pull-left::text").get()
        body = sel.css(".panel-body div")
        tables = body.css("table").getall()

        data = {
            **response.meta,
            "major_extra": major_extra,
            "tables": tables
        }
        yield data
  