# -*- coding: utf-8 -*-
import scrapy


class SpecialOffersSpider(scrapy.Spider):
    name = 'special_offers'
    #allowed_domains = ['www.cigabuy.com/specials.html']
    allowed_domains = ['www.cigabuy.com']
    #start_urls = ['http://www.cigabuy.com/specials.html/']
    #start_urls = ['https://www.cigabuy.com/specials.html/'] # retirei o / do final, https

    ##start_urls = ['https://www.cigabuy.com/consumer-electronics-c-56_75-pg-1.html']

    def start_requests(self):
        yield scrapy.Request(
            url = 'https://www.cigabuy.com/consumer-electronics-c-56_75-pg-1.html', 
            callback = self.parse, 
            headers = {
                'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
            })

    def parse(self, response):
        for product in response.xpath("//div[@class='r_b_c']/div[@class='p_box_wrapper']"):
            yield {
                'title':product.xpath(".//div/a[@class='p_box_title']/text()").get(),
                'url': product.xpath(".//div/a[@class='p_box_title']/@href").get(),
                'discoutned_price':product.xpath(".//div/div[@class='p_box_price cf']/span[@class='productSpecialPrice fl']/text()").get(),
                'normal_price':product.xpath(".//div/div[@class='p_box_price cf']/span[@class='normalprice fl']/text()").get(),
                'User-Agent': response.request.headers['User-Agent']
            }


        next_page = response.xpath("//a[@class='nextPage']/@href").get()

        if next_page:
            yield scrapy.Request(url = next_page, 
            callback = self.parse,
            headers = {
                'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
            })

    
    
    
    #user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36


    # def parse(self, response):
    #     for product in response.xpath("//div[@class='p_box_wrapper']"):
    #         yield {
    #             'title': product.xpath(".//a[@class='p_box_title']/text()").get(),
    #             'url': response.urljoin(product.xpath(".//a[@class='p_box_title']/@href").get()),
    #             'discoutned_price': product.xpath(".//div[@class='p_box_price']/span[1]/text()").get(),
    #             'original_price': product.xpath(".//div[@class='p_box_price']/span[2]/text()").get(),
    #         }

    # 
