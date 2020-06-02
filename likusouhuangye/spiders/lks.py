# -*- coding: utf-8 -*-
import scrapy
from ..items import LikusouhuangyeItem
import re


class LksSpider(scrapy.Spider):
    name = 'lks'
    allowed_domains = ['likuso.com']
    start_urls = ['http://www.likuso.com/']
    base_url = 'http://www.likuso.com'

    def parse(self, response):
        citys_url = response.xpath('//div[@class="allcpy"]/ul/li/a/@href').getall()
        for city_url in citys_url:
            yield scrapy.Request(url=city_url, callback=self.parse_company_list)

    def parse_company_list(self, response):
        errors = re.findall(r'searchd error: offset out', response.text)
        coms = response.xpath('//h2[@class="clearfix"]/a/@href').getall()
        country_name = response.xpath('//ul[@id="s_tag_city"]/li[1]/a/text()').get()
        for com in coms:
            meta = {
                'country_name': country_name
            }
            yield scrapy.Request(url=com, callback=self.parse_detail, meta=meta)

        countrys = response.xpath('//ul[@id="s_tag_city"]/li/a/@href').getall()
        for country in countrys:
            if country[0] == '/':
                country = self.base_url + country
            yield scrapy.Request(url=country, callback=self.parse_company_list)
        if len(errors) != 0:
            print(errors[0])
            next_page = response.xpath('//div[@class="pager-nav"]/a[@title="下一页"]/@href').get()
            yield scrapy.Request(url=next_page, callback=self.parse_company_list)
        else:
            print('errors', errors)

    def parse_detail(self, response):
        item = LikusouhuangyeItem()
        country_name = response.meta['country_name']
        quancheng = '无'
        zhucediqu = '无'
        lianxiren = '无'
        dianhua = '无'
        shouji = '无'
        address = '无'
        infos = response.xpath('//div[@class="base_info"]/ul/li')

        for info in infos:
            if info.xpath('span/text()').get() == '全称：':
                quancheng = info.xpath('text()').get().strip()

            if info.xpath('span/text()').get() == '注册地区：':
                zhucediqu = info.xpath('text()').get().strip()

            if info.xpath('span/text()').get() == '联系人：':
                lianxiren = info.xpath('text()').get().strip()
            if info.xpath('span/text()').get() == '电话：':
                dianhua = info.xpath('text()').get().strip()

            if info.xpath('span/text()').get() == '手机：':
                shouji = info.xpath('text()').get().strip()[:11]

            if info.xpath('span/text()').get() == '经营地址：':
                address = info.xpath('text()').get().strip()

        item['quancheng'] = quancheng
        item['zhucediqu'] = zhucediqu
        item['lianxiren'] = lianxiren
        item['dianhua'] = dianhua
        item['shouji'] = shouji
        item['country_name'] = country_name
        item['address'] = address
        print(item)
        yield item
