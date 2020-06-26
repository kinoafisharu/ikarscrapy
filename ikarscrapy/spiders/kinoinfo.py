# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class KinoinfoSpider(scrapy.Spider):
    name = 'kinoinfo'

    def start_requests(self):
        urls = [f'http://kinoinfo.ru/film/{i}/' for i in range(1, 46000)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)



    def __get_kid(self, response):
        ex = re.search(r'[-+]?\d+', response.url)
        return ex.group() if ex else None

    def __parse_release(self, response):
        release = response.xpath('/html/body/div[1]/div/div[3]/div/div[2]/div/div[1]/div[11]/span[3]/@title').get()
        if release:
            srelease = str(release)
            relreg = re.search(r'\d{,2}\s\w{1,13}\s\d{,4}', srelease)
            if relreg and relreg.group() == srelease:
                return release
            else:
                release = response.xpath('/html/body/div[1]/div/div[3]/div/div[2]/div/div[1]/div[11]/span[2]/@title').get()
                return release
        return None


    def parse(self, response):
        item = {}
        item['kid'] = self.__get_kid(response)
        item['release'] = self.__parse_release(response)

        yield item if item['release'] != None else None
