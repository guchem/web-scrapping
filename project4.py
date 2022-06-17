import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import pandas as pd

date, home,score,away  = [], [], [], []

class Project4Spider(CrawlSpider):
    name = 'project4'
    allowed_domains = ['www.adamchoi.co.uk']
    dscript = '''
        function main(splash, args)
            splash: on_request(function(request)
                request: set_header('User-Agent',
                        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36')
            end)
            splash.private_mode_enabled = false
            assert(splash:go(args.url))
            assert(splash:wait(3))
            all_matches = assert(splash:select_all("label.btn.btn-sm.btn-primary"))
            all_matches[2]:mouse_click()
            assert(splash:wait(3))
            splash:set_viewport_full()
          r eturn {splash:png(), splash:html()}
        end
    '''

    def start_requests(self):
        yield SplashRequest(url='https://www.adamchoi.co.uk/overs/detailed', callback=self.parse,
                            endpoint='execute', args={'lua_source':self.script})

    def parse(self, response):
        rows = response.xpath('//tr')
        for row in rows:
            date.append(row.xpath('./td[1]/text()').get())
            home.append(row.xpath('./td[2]/text()').get())
            score.append(row.xpath('./td[3]/text()').get())
            away.append(row.xpath('./td[4]/text()').get())

        df_matches = pd.DataFrame({'Date': date,'Home team':home,'Score':score, 'Away team':away})
        df_matches.to_csv('project4_matches.csv', index=False)
