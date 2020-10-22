# Web Scrap com scrapy

* Para baixar fotos, vídeos, arquivos, textos.

## Scrapy

#### Spider
    Definir o que se quer baixar.

##### Classes - Divididas em 5. Só abordarei as duas primeiras.
1. scrapy.Spider
1. CrawlSpider
1. XMLFeedSpider
1. CSVFeedSpider
1. SitemapSpider

#### Pipelines
* Sequência de manipução de dados. Manipular dados e salvar.

#### Middlewares
* Request/Response
* Injectin custom header
* Proxying

#### Engine
* Coordena as ações

#### Scheduler
* Preserva a ordenação das ações, resquests

#### Fluxo de operação
1. Spider - resquest
2. Engine - resquest
3. Scheduler - resquest
4. Engine - resquest
5. Middleware - Downloader Middleware - response
6. Spider - Spider Middleware - extract data
7. Engine
8. Pipeline

## Robots.txt
    Instrução do que pode ou não pode ser baixado, exemplo: https://www.facebook.com/robots.txt
* User-Agent
* Allow
* Disallow - Páginas proibidas

## Instalação:
* conda install -c conda-forge scrapy==1.6
* pylint 
* autopep8
* Outra alternativa
  * python3 -m pip install scrapy==1.6 pylint autopep

## Terminal
* scrapy - Abre a ferramenta
* scrapy bench - Benchmark test
* scrapy fetch http://google.com
* scrapy version - Versão do scrapy
* scrapy startproject nomedoprojeto
* shell - Para fazer experimentos
* runspider - Usado para executar spider sem criar projeto, bom para projetos rápidos e testes

## Primeiro Scrap
    Scrap da página https://www.worldometers.info/world-population/population-by-country/

1. scrapy startproject worldometers - Criar projeto worldometers
1. Ir para pasta worldometers
1. Criar spider
    - scrapy genspider countries www.worldometers.info/world-population/population-by-country 
    - Precisa apagar a última barra(/) porque o scrapy adiciona automaticamente e também apagar o https://
    - Countries é o nome do spider, o nome deve ser único
2. Alterar de http para https em spider/country.py
3. conda install ipython 
    - Instalar ipython ou pip install ipython
4. scrapy shell
    - Dentro do scrapy shell o comando shelp() mostra o help
    - Abre o shell para fazer alguns testes
    - scrapy shell site - Se fosse informado o site já baixaria a página com apenas 1 passo.
5. fetch("https://www.worldometers.info/world-population/population-by-country/")
    - Digitar dentro do shell 
    - No caso não achou o robots.txt então não há restrição alguma.
6. r = scrapy.Request(url = "https://www.worldometers.info/world-population/population-by-country/")
    - Cuidado com o nome da variável no shell, escolha algo simples.
    - com esse objeto é possível passar para o fetch, dessa forma, existem duas formas para informar o indereço para o fetch, para o 'buscador'.
7. fetch(r)
8. response.body
    - Vai carregar toda html
9.  view(response)
    - Abre uma página da página baixada. Não é a forma mais recomendada para visualizar a página.
    - O recomendável é abrir a página e desativar o javascript. No inspetor e desativar o javascript para observar como o scrapy baixa  página.
    - Ctrl + shift + i 
    - Ctrl + shilt + p
    - Desabilitar javascript - Obs: Spiders não renderizam javascript.

10. Scrap do título
    - Ctrl + F dentro da janela inspecionar
    - Dentro do navegador buscar o título usando xpath: "//h1"

11. De volta ao terminal.
    - title = response.xpath('//h1') - Retorna o texto com a tag h1
    - title = response.xpath('//h1/text()') - Usando a função text() retira o texto da tag
    - title.get() - Mostra o conteúdo da tag h1
    - usando css
        - title_css = response.css('h1::text')
        - title_css.get() - Mostra o conteúdo da tag h1

12. Agora buscar os países.
    Aqui no caso é usado .getall() porque é uma lista de dados
    - countries = response.xpath('//td/a/text()').getall()
    - countries_css = response.css('td a::text').getall()

13. Alterar o spider countries.py

```
class CountriesSpider(scrapy.Spider):
    name = 'countries' # Esse nome é único, é possível ter diversas spiders mas cada uma tem que ter um nome diferente caso contrário criará um conflito
    #allowed_domains = ['www.worldometers.info/world-population/population-by-country']
    allowed_domains = ['www.worldometers.info'] #limita o escopo do spider, não pode ter o http://
    #start_urls = ['http://www.worldometers.info/world-population/population-by-country/']
    start_urls = ['https://www.worldometers.info/world-population/population-by-country/'] #Todos os links que queremos buscar, mudei para https por causa do site
``` 
    #### É bom lembrar que o padrão name, allowed_domains, start_urls, parse são nomes padrões, se forem trocados não irá funcionar
    
    def parse(self, response):
        #pass
        title = response.xpath('//h1/text()').get()
        countries = response.xpath('//td/a/text()').getall()

        # retornar como dicionário
        yield {
            'title':title,
            'countries':countries
        }

14. No terminal - rodar o spider countries, precisa ser no mesmo nível que está o arquivo scrapy.cfg
    1.  scrapy crawl countries

## XML-Path Language e CSS-Cascading Style Sheet

### CSS Seletor

#### Selecionando pelas tags

    Site para testes - https://try.jsoup.org/

    Usa "." busca por atributos das classes.
     <div class ='intro'>
     .nomedaclasse
     .intro

    Usa "#" busca por atributos das ids.
     <div id ='location'>
     #nomedaid
     #location
    
    Para acessar tag dentro de uma tag específica, por exemplo, uma div.
     tag.atributo
     tag#location
     .bold.italic  
        <p class="bold italic">Hi, I have two classes</p>

Para múltiplas classes e ids
    
     .class.class
     #id#id

Se a class nao é padrão do html e foi criada, para selecionar é um pouco diferente:

     li[data-identifier=7]  ou [data-identifier=7] 
        <li data-identifier="7">Item 1</li> 

Para selecionar apenas atributos de classe que começam com https, usando ^.

     a[href^='https']
        <a href="https://www.google.com">

Aqui os atributos que terminam com algum texto, usando $. Lembre-se de regex.

     a[href$='fr']
        <a href="http://www.google.fr">

É possível buscar qualquer atributos em tag que começam com outros parametros também, por exemplo:

     [class^='in']

É possível achar a parte do meio de um atributo de classe também, usando *.

     a[href*='google']
        <a href="http://www.google.fr">

Se não quer selecionar algo aparece no início e nem no final, usando ~.

     a[href~='fr']      obs: Não funcionou no teste.

#### Como selecionar pela posição?

Selecionar dos os p dentro da div e da classe intro. Não pega os descendentes das tags que estão dentro:

     div.intro p
    
Se for necessário pegar um descente específico, basta informar:

     div.intro p, span#location

Se for necessário pegar todos os descentes da div, classe intro e tag p:

     div.intro > p

Para pegar a tag p imidiatamente depois da div com classe intro, só serve se estiver imediatamente depois da div, caso contrário não retornará nada. + span não retornará nada.

     div.intro + p

Seleciona item da lista que está no índice 1.

     li:nth-child(1)
  
Seleciona os índices ímpares.

     li:nth-child(odd)

Seleciona os índices ímpares.

     li:nth-child(even)

#### Selecionando com Xpath

Xpath é melhor que permite ir para frente e para trás em um texto html

Site para testes: https://scrapinghub.github.io/xpath-playground/

Para selecionar tags com Xpath é necessário dupla barra na frente primeiro

Procura todas h1 na html

    //h1

    //div[@class='intro']

    //div[@class='intro']/p

    //div[@class='intro' or @class='outro']/p

    //div[@class='intro' or @class='outro']/p/text()

    //a/@href

    //a[starts-with(@href, 'https')]

    //a[ends-with(@href, 'fr')]   Vai retornar erro porque só suporta a partir da versão 2.0. Não vai funcionar nos browsers.

    //a[contains(@href, 'google')]

    //a[contains(text(), 'France')] Busca no texto e não na tag. É case sensitive.

#### Selecionar pela posição

        li[1]

        //ul[@id='items']/li[position() = 1 or position() =4 ]

        //ul[@id='items']/li[position() = 1 or position() =last() ]

        //ul[@id='items']/li[position() > 1 ]

#### Navegar para cima e para baixo na html usando axes. CSS não tem essa função.

##### Para cima

        //p[@id='unique']/parent::div

        //p[@id='unique']/parent::node()

        //p[@id='unique']/ancestor::node()

        //p[@id='unique']/ancestor-or-self::node()

        //p[@id='unique']/preceding::node()

        //p[@id='unique']/preceding::h1

        //p[@id='outside']/preceding-sibling::node()

##### Para baixo

    //div[@class='intro']/p

    //div[@class='intro']/child::p

    //div[@class='intro']/child::node()

    //div[@class='intro']/following::node()

    //div[@class='intro']/following-sibling::node()

    //div[@class='intro']/descendant::node()


#### Comparação entre xpath e css

In [41]: response.xpath('//tbody/tr/td/a[@href]/text()')[0]
Out[41]: <Selector xpath='//tbody/tr/td/a[@href]/text()' data='China'>

In [42]: response.css('tbody tr td a[href]::text')[0]
Out[42]: <Selector xpath='descendant-or-self::tbody/descendant-or-self::*/tr/descendant-or-self::*/td/descendant-or-self::*/a[@href]/text()' data='China'>


Leia - https://escoladedados.org/tutoriais/xpath-para-raspagem-de-dados-em-html/#:~:text=Basta%20selecionar%20o%20texto%20que,a%20op%C3%A7%C3%A3o%20'Copiar%20XPath'.&text=Esta%20fun%C3%A7%C3%A3o%20%C3%A9%20interessante%2C%20mas,ter%20express%C3%B5es%20leg%C3%ADveis%20ou%20curtas.

* Para exportar 
        
        scrapy crawl countries -o population_dataset.json

            No vscode alt+shift+f formata o json automaticamente.

        scrapy crawl countries -o population_dataset.csv

        scrapy crawl countries -o population_dataset.xml
        
        
## Scraping múltiplas páginas

    spider cigabuy

https://www.cigabuy.com/consumer-electronics-c-56_75-pg-1.html

scrapy startproject cigabuy
scrapy genspider special_offers www.cigabuy.com/specials.html

Alterar para https

* testes: 

scrapy shell https://www.cigabuy.com/consumer-electronics-c-56_75-pg-1.html

 response.xpath("//div[@class='r_b_c']").xpath(".//div[@class='p_box_wrapper']").css("div").xpath("a[@class='p_box_title']/text()").getall()

 response.xpath("//div[@class='r_b_c']").xpath(".//div[@class='p_box_wrapper']").css("div").css("a.p_box_title::text").getall()

 response.xpath("//div[@class='r_b_c']").xpath(".//div[@class='p_box_wrapper']").css("div").css("a.p_box_title::attr(href)").getall()

 response.xpath("//div[@class='r_b_c']").xpath(".//div[@class='p_box_wrapper']").css("div").xpath("a[@class='p_box_title']/@href").getall()

scrapy crawl special_offers -o dataset_encoding.json


* Pode har problemas de encoding no json por isso, alterar em settings.py: 

    FEED_EXPORT_ENCODING = 'utf-8'

* Alterar user-agent no spider cigabuy tem algumas formar como solução.
    
    user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36

## Debug

#### Parse Command

scrapy parse --spider=countries -c parse_country --meta='{"country_name":"China"}' https://www.worldometers.info/world-population/china-population/

#### scrapy shell

#### Open in browser

#### Debug com o arquivo runner.py que está no projeto cigabuy.

* Possibilidade para salvar arquivo.csv sem linha de comando:
    *  FEED_FORMAT
    *  FEED_URI

```
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from worldometers.spiders.countries import CountriesSpider


#process = CrawlerProcess(settings=get_project_settings())

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)', 
    'FEED_FORMAT': 'CSV', 
    'FEED_URI': '~/export_vscode.csv',
})

process.crawl(CountriesSpider)
process.start()

```