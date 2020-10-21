# -*- coding: utf-8 -*-
import scrapy


class SpecialOffersSpider(scrapy.Spider):
    name = 'special_offers'
    #allowed_domains = ['www.cigabuy.com/specials.html']
    allowed_domains = ['www.cigabuy.com']
    #start_urls = ['http://www.cigabuy.com/specials.html/']
    #start_urls = ['https://www.cigabuy.com/specials.html/'] # retirei o / do final, https

    start_urls = ['https://www.cigabuy.com/consumer-electronics-c-56_75-pg-1.html']

    def parse(self, response):
        for product in response.xpath("//div[@class='r_b_c']/div[@class='p_box_wrapper']"):
            yield {
                'title':product.xpath(".//div/a[@class='p_box_title']/text()").get(),
                'url': product.xpath(".//div/a[@class='p_box_title']/@href").get(),
                'discoutned_price':product.xpath(".//div/div[@class='p_box_price cf']/span[@class='productSpecialPrice fl']/text()").get(),
                'normal_price':product.xpath(".//div/div[@class='p_box_price cf']/span[@class='normalprice fl']/text()").get()
            }




    # def parse(self, response):
    #     for product in response.xpath("//div[@class='p_box_wrapper']"):
    #         yield {
    #             'title': product.xpath(".//a[@class='p_box_title']/text()").get(),
    #             'url': response.urljoin(product.xpath(".//a[@class='p_box_title']/@href").get()),
    #             'discoutned_price': product.xpath(".//div[@class='p_box_price']/span[1]/text()").get(),
    #             'original_price': product.xpath(".//div[@class='p_box_price']/span[2]/text()").get(),
    #         }

    