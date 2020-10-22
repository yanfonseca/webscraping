# -*- coding: utf-8 -*-
import scrapy
# importados
#import logging
#from scrapy.shell import inspect_response
#from scrapy.utils.response import open_in_browser

class CountriesSpider(scrapy.Spider):
    name = 'countries' 
    # O ome é único, é possível ter diversos spiders mas cada um com um nome diferente caso contrário haverá conflito
    #allowed_domains = ['www.worldometers.info/world-population/population-by-country']
    allowed_domains = ['www.worldometers.info'] # Não pode ter / no fim. Limita o escopo de atuação do spider, não pode ter o http://
    #start_urls = ['http://www.worldometers.info/world-population/population-by-country/']
    start_urls = ['https://www.worldometers.info/world-population/population-by-country/'] #Todos os links que queremos buscar, mudei para https por causa do site
     # name, allowed_domains, start_urls, parse são variáveis padrão, o scrapy reconhece essas variáveis
    
    def parse(self, response):
        #pass
        #title = response.xpath('//h1/text()').get()
        #countries = response.xpath('//td/a/text()').getall()

        countries = response.xpath('//td/a')

        for country in countries:
            # response.xpath('//td/a/text()') retorna um selector que por sua vez getall() extrai o texto
            # Executar outra xpath function em selector object e não em um response, então é necessário
            # iniciar com .//
            name = country.xpath('.//text()').get()

            # extrai uma url relativa, sem o domain, no scray shell usaria o fetch() mas aqui não pode 
            link = country.xpath('.//@href').get() 
            
            #yield scrapy.Request(url = link ) retorna erro
            
            # 1 forma de acessar a url
            #absolute_url = f'https://www.worldometers.info{link}'
            #yield scrapy.Request(url = absolute_url) 
            
            # 2 forma
            #absolute_url = response.urljoin(link)
            #yield scrapy.Request(url = absolute_url) 
            
            # 3 forma - ja acrescenta o domain a url relativa
            # cada reponse é enviada para parse_Country, só que dessa forma ainda não é possível acessar nome de dentro de parse_country
            #yield response.follow(url = link, callback = self.parse_country)

            # 4 forma com o parse_country
            # meta é um dicionário
            yield response.follow(url = link, callback = self.parse_country, meta = {'country_name':name})

        # retornar como dicionário
        #    yield {
                #'title':title,
        #    'country_name': name,
        #   'country_link': link
        #}

    def parse_country(self, response):
        #logging.info(response)
        #inspect_response(response, self)
        #open_in_browser(response)
        #logging.info(response.status)
        name = response.request.meta['country_name']
        rows = response.xpath("(//table[@class='table table-striped table-bordered table-hover table-condensed table-list'])[1]/tbody/tr")

        for row in rows:
            year = row.xpath('.//td[1]/text()').get()
            population = row.xpath('.//td[2]/strong/text()').get()

            yield {
                'country_name': name,
                'year': year, 
                'population': population
            }
