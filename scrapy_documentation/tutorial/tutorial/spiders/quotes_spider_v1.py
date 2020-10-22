import scrapy


class QuotesSpider(scrapy.Spider):
    
    name = "quotes_v1"
    
    def start_requests(self):
        urls = [
            'http://quotes.toscrape.com/page/1/',
            'http://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_alterada)
    
    #mudei o nome padrão de parse para parse_alterada, então, é necessário informar a callback
    def parse_alterada(self, response):
        page = response.url.split("/")[-2]
        filename = f'quotes-{page}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')
