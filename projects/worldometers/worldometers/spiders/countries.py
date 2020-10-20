# -*- coding: utf-8 -*-
import scrapy


class CountriesSpider(scrapy.Spider):
    name = 'countries' # Esse nome é único, é possível ter diversas spiders mas cada uma tem que ter um nome diferente caso contrário criará um conflito
    #allowed_domains = ['www.worldometers.info/world-population/population-by-country']
    allowed_domains = ['www.worldometers.info'] #limita o escopo do spider, não pode ter o http://
    #start_urls = ['http://www.worldometers.info/world-population/population-by-country/']
    start_urls = ['https://www.worldometers.info/world-population/population-by-country/'] #Todos os links que queremos buscar, mudei para https por causa do site
    
    # É bom lembrar que o padrão name, allowed_domains, start_urls, parse são nomes padrões, se forem trocados não irá funcionar
    
    def parse(self, response):
        #pass
        #title = response.xpath('//h1/text()').get()
        countries = response.xpath('//td/a/text()').getall()

        # retornar como dicionário
        yield {
            'title':title,
            'countries':countries
        }