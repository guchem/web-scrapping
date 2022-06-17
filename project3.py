import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import pandas as pd

titles = []
plots = []
transcriptions = []
urls = []
class Project3Spider(CrawlSpider):
   
    name = 'project3'
    allowed_domains = ['subslikescript.com']
    start_urls = ['https://subslikescript.com/movies_letter-X']  # let's test scraping all the pages for the X letter

    rules = (
        Rule(LinkExtractor(restrict_xpaths=("//ul[@class='scripts-list']/a")), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths=("(//a[@rel='next'])[1]"))),
    )

    def parse_item(self, response):
        article = response.xpath("//article[@class='main-article']")
        
        titles.append(article.xpath("./h1/text()").get())
        plots.append(article.xpath("./p/text()").get())
        transcriptions.append(article.xpath("./div[@class='full-script']/text()").getall())
        urls.append(response.url)


        df_articles = pd.DataFrame({'title': titles,'plot':plots,'transcription':transcriptions, 'url':urls})
        df_articles.to_csv('project3_transcript.csv', index=False)
