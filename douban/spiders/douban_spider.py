import scrapy
from douban.items import DoubanItem

class DoubanSpiderSpider(scrapy.Spider):
    # 爬虫名称
    name = 'douban_spider'
    # 允许域名
    allowed_domains = ['movie.douban.com']
    # 入口url
    start_urls = ['https://movie.douban.com/top250']

    # 数据解析
    def parse(self, response):
        movie_list = response.xpath("//div[@class='article']//ol[@class='grid_view']//li")
        for item in movie_list:
            douban_item = DoubanItem()
            douban_item['serial_number'] = item.xpath(".//div[@class='pic']/em/text()").extract_first()
            douban_item['movie_name'] = item.xpath(".//div[@class='hd']/a/span[1]/text()").extract_first()
            content = item.xpath(".//div[@class='bd']/p[1]/text()").extract()
            content_s = ''
            for i_content in content:
                content_s = content_s + ''.join(i_content.split())
            douban_item['introduce'] = content_s
            douban_item['star'] = item.xpath(".//span[@class='rating_num']/text()").extract_first()
            douban_item['evaluate'] = item.xpath(".//div[@class='star']/span[4]/text()").extract_first()
            douban_item['describe'] = item.xpath(".//p[@class='quote']/span/text()").extract_first()
            # yield到pipeline,settings中需要启用
            yield douban_item
        # 下一页的数据
        next_link = response.xpath("//span[@class='next']//link/@href").extract()
        if next_link:
            # 递归将下一页的地址传给这个函数自己，在进行爬取
            yield scrapy.Request("https://movie.douban.com/top250" + next_link[0], callback=self.parse)