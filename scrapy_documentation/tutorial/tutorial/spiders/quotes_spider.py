import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
        'http://quotes.toscrape.com/page/2/',
    ]

#    def start_requests(self):
#        urls = [
#            'http://quotes.toscrape.com/page/1/',
#            'http://quotes.toscrape.com/page/2/',
#        ]
        
#	 parse()  é chamado é default para o callback, não precisa escrever explicitamente
	#for url in urls:
#            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f'quotes-{page}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')
