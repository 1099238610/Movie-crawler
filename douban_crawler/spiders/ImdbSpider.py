import scrapy
from douban_crawler.items import MovieItem


class DoubanMovieSpider(scrapy.Spider):
    name = "IMDB"
    allowed_domains = ['imdb.com']
    start_urls = ['https://www.imdb.com/search/title/?title_type=feature&release_date=2017-01-01,'
                  '2018-12-31&sort=moviemeter,asc']

    def start_requests(self):
        # 设置请求头, 避免反爬
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/58.0.3029.110 Safari/537.36',
        }
        for url in self.start_urls:
            yield scrapy.Request(url, headers=headers, callback=self.parse)

    def parse(self, response):
        for movie in response.css('div.ipc-metadata-list-summary-item__c'):
            # 获取电影细节信息, 为长度固定为 3 的数组, 格式为[年份, 时长, 分级]
            dli_title = movie.css('div.sc-479faa3c-7.jXgjdT.dli-title-metadata span::text').extract()

            yield {
                'title': movie.css('h3.ipc-title__text::text').get(),
                'rating': movie.css('span.ipc-rating-star.ipc-rating-star--base.ipc-rating-star--imdb.ratingGroup'
                                    '--imdb-rating::attr(aria-label)').get(),
                'year': dli_title[0],
                'duration': dli_title[1],
                # 美国电影分级
                'MPA_rating': dli_title[2],
            }

        next_page = response.css('div.desc > a::attr(href)').extract_first()

        if next_page:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(url=next_page, callback=self.parse)
