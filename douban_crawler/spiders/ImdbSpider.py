import time

import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from douban_crawler.items import MovieItem


class DoubanMovieSpider(scrapy.Spider):
    name = "IMDB"
    allowed_domains = ['imdb.com']
    start_urls = ['https://www.imdb.com/search/title/?title_type=feature&sort=release_date,asc']

    def start_requests(self):
        # 设置请求头, 避免反爬
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/58.0.3029.110 Safari/537.36',
        }
        for url in self.start_urls:
            yield scrapy.Request(url, headers=headers, callback=self.parse)

    def parse(self, response):

        # 初始化
        option = webdriver.ChromeOptions()
        # 设置为无界面
        # option.add_argument('--headless')
        option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, "
                            "like Gecko) Chrome/58.0.3029.110 Safari/537.36")
        driver = webdriver.Chrome(options=option)
        count = 0

        # 打开网页
        driver.get(response.url)

        try:
            while count < 100:

                # 等待按钮可见
                wait = WebDriverWait(driver, 10)

                # 等待新数据加载完成（根据实际情况调整等待条件）
                wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div.ipc-metadata-list-summary-item__c'))
                )

                for movie in driver.find_elements(By.CSS_SELECTOR, 'div.ipc-metadata-list-summary-item__c')[-50:]:
                    count += 1

                    title = movie.find_element(By.CSS_SELECTOR, 'h3.ipc-title__text').text
                    print("count: {}, movie: {}".format(count, title))

                    # 获取电影细节信息, 为长度固定为 3 的数组, 格式为[年份, 时长, 分级]
                    dli_title = movie.find_element(By.CSS_SELECTOR,
                                                   'div.sc-479faa3c-7.jXgjdT.dli-title-metadata')
                    span_elements = dli_title.find_elements(By.CSS_SELECTOR, 'span')
                    span_texts = [span.text for span in span_elements]
                    print(span_texts)
                    # 存储数据
                    yield {
                        'title': title,
                        'IMDB_rating': movie.find_element(By.XPATH,
                                                     '//span[contains(@class, "ratingGroup--imdb-rating")]')
                        .get_attribute('aria-label'),

                        'year': span_texts[0] if span_texts[0] else None,
                        'duration': span_texts[1] if len(span_texts) > 1 else None,
                        'MPA_level': span_texts[2] if len(span_texts) > 2 else None,
                    }

                # 获取按钮
                button = wait.until(
                    EC.visibility_of_element_located((By.XPATH, '//button[contains(@class, "ipc-see-more__button")]'))
                )

                # 使用execute_script平滑滚动到页面底部
                driver.execute_script("arguments[0].scrollIntoView(true);", button)

                # 模拟点击按钮
                button.click()

                time.sleep(10)
        finally:
            # 关闭浏览器窗口
            driver.quit()
