import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes_v3"
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
    ]

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }

        next_page = response.css('li.next a::attr(href)').get()
        # if next_page is not None:
        #     next_page = response.urljoin(next_page) 
        #     yield scrapy.Request(next_page, callback=self.parse) # 1 opção

        # if next_page is not None: 
        #     yield response.follow(next_page, callback=self.parse)  # 2 opção - com o follow

        # for href in response.css('ul.pager a::attr(href)'):
        #     yield response.follow(href, callback=self.parse) # 3 opção - passando um atributo de um seletor
        
        # for a in response.css('ul.pager a'):
        #     yield response.follow(a, callback=self.parse) # 4 opção - forma mais resumida


        anchors = response.css('ul.pager a')
        yield from response.follow_all(anchors, callback=self.parse) # opção - múltiplos requests através de um iterável

        # ou ainda
        #yield from response.follow_all(css='ul.pager a', callback=self.parse)