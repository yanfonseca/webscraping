import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from worldometers.spiders.countries import CountriesSpider


#process = CrawlerProcess(settings=get_project_settings())

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)', 
    'FEED_FORMAT': 'CSV', 
    'FEED_URI': '/mnt/c/Users/yanfo/projetos_python/webscraping/projects/worldometers/export_vscode.csv',
})

process.crawl(CountriesSpider)
process.start()