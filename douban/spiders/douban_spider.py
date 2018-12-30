# -*- coding: utf-8 -*-
import scrapy
from douban.items import DoubanItem
'''
第一步 在cmd更新spider
scrapy genspider douban_spider movie.douban.com
'''
'''
第三步骤 改写spider
'''
class DoubanSpiderSpider(scrapy.Spider):
    #爬虫名和项目名称不重复
    name = 'douban_spider'
    #允许的域名
    allowed_domains = ['movie.douban.com']
    #入口url 将url扔到调度器里面 目标网页
    start_urls = ['https://movie.douban.com/top250']
    #看是否进行请求数据
    '''
    
    
    fourth:cmd中 scrapy crawl douban_spider(name)
    watch revelant info in cmd
    在信息里面显示 403 
    parse:中测试
    print (response.text)
    DEBUG: Crawled (403) <GET https://movie.douban.com/robots.txt> (referer: None)
    在setting里面UA需要改写
    在网页里面 networks界面 找到ua 保存后重新load
    scrapy crawl douban_spider
    5th：建立main函数 在charm进行抓取网页
    '''

    '''
    6th：进行解析文件 xpath html节点
    '''
    def parse(self, response):
        #这个爬取的是25个general 大框架 接着细匹配
        movie_list = response.xpath("//div[@class='article']//ol[@class='grid_view']/li")
        for i_item in movie_list:
            #导入item 进行创建变量 保存数据
            douban_item = DoubanItem()
            #进行更细的编写 解析到第一个语句中
            douban_item['serial_number'] = i_item.xpath(".//div[@class='item']//em/text()").extract_first()
            #7th 编写好 进行测试 print (douban_item) 在main函数里面进行检测
            douban_item['movie_name'] = i_item.xpath(".//div[@class='info']/div[@class='hd']/a/span[1]/text()").extract_first()
            #需要解析的数据 不是第一行 而是好几行
            content = i_item.xpath(".//div[@class='bd']//p[1]/text()").extract()
            ##由于介绍部分 有很多行 需要进一步处理
            for i_content in content:#处理空格
                content_s = "".join(i_content.split())
                douban_item['introduce'] = content_s
            douban_item['star'] = i_item.xpath(". //div[@class='star']/span[@class='rating_num']/text()").extract_first()
            douban_item['evaluate'] = i_item.xpath(".//div[@class='star']//span[4]/text()").extract_first()
            douban_item['describe'] = i_item.xpath(".//p[@class='quote']/span[1]/text()").extract_first()
            #第一页数据 yield 到管道中 pipeline中 downloader进行数据解析
            yield  douban_item
            #8 th 判断有没有新的request请求 需要解析后一页
         #next page需要写到外面的for中
        next_link = response.xpath("//span[@class='next']//link/@href").extract()
        #所有的都结束了
        if next_link:
            next_link = next_link[0]
            yield  scrapy.Request("https://movie.douban.com/top250"+next_link,callback=self.parse)
        print(douban_item)
        #保存到数据 scrapy crawl douban_spider -o test.json