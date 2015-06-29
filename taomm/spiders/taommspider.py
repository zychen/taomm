#!/usr/bin/env python
# coding=utf-8
"""
File: taommspider.py
Author: CHENZY
Date: 2015/06/25
"""
import scrapy
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy import cmdline
from taomm.items import TaommItem


class TaoMMSpider(scrapy.Spider):
    name = 'taoMM'
    page = 1
    start_urls = []
    while page < 4316:
        start_urls.append('http://mm.taobao.com/json/request_top_list.htm?page=%s' % str(page))
        page += 1

    def parse(self, response):
        sel = Selector(response)

        # totalPage = sel.xpath('//*[@id="J_Totalpage"]/@value').extract()[0]
        ladyList = sel.xpath('//div[@class="personal-info"]')

        for lady in ladyList:
            Lady = TaommItem()
            Lady['nickname'] = lady.xpath('.//a[@class="lady-name"]/text()').extract()[0]
            Lady['age'] = lady.xpath('.//p[@class="top"]/em/strong/text()').extract()[0]
            Lady['city'] = lady.xpath('.//p[@class="top"]/span/text()').extract()[0]
            Lady['fans'] = lady.xpath('.//p[2]/em/strong/text()').extract()[0]
            Lady['occupation'] = lady.xpath('.//p[2]/em[1]/text()').extract()[0]
            Lady['homepageUrl'] = 'http:' + lady.xpath('.//a[@class="lady-name"]/@href').extract()[0]
            Lady['detail'] = '昵称：%s\n年龄：%s，城市：%s，粉丝数：%s\n职业：%s\n个人主页：%s' % (Lady['nickname'], Lady['age'], Lady['city'], Lady['fans'], Lady['occupation'], Lady['homepageUrl'])
            detailUrl = 'http:' + lady.xpath('.//div[@class="pic s60"]/a/@href').extract()[0]

            if int(Lady['fans']) > 9999:
                yield Request(url=detailUrl, callback=self.parse_details, meta={'Lady': Lady})
                continue

    def parse_details(self, response):
        Lady = response.meta['Lady']
        sel = Selector(response)
        aixiuContent = sel.xpath('//div[@id="J_ScaleImg"]')[0]
        Lady['image_urls'] = aixiuContent.xpath('.//img/@src').extract()
        return Lady




if __name__ == '__main__':
    cmdline.execute("scrapy crawl taoMM -s JOBDIR=crawls/somespider-1".split())


