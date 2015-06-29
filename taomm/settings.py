# -*- coding: utf-8 -*-

# Scrapy settings for taomm project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'taomm'

SPIDER_MODULES = ['taomm.spiders']
NEWSPIDER_MODULE = 'taomm.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'taomm (+http://www.yourdomain.com)'

# 设置代理
DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
    'taomm.middlewares.ProxyMiddleware': 100,
}

# 访问页面延时
DOWNLOAD_DELAY = 10
# 将访问页面延时时间设置成随机，随机值=random(0.5, 1.5) * DOWNLOAD_DELAY
RANDOMIZE_DOWNLOAD_DELAY = True

# 对单个网站进行并发请求的最大值
CONCURRENT_REQUESTS_PER_DOMAIN = 1

# Scrapy downloader 并发请求(concurrent requests)的最大值
CONCURRENT_REQUESTS = 1

# 过滤小图片
IMAGES_MIN_HEIGHT = 550
IMAGES_MIN_WIDTH = 550

# 下载图片
ITEM_PIPELINES = {
    # 'scrapy.contrib.pipeline.images.ImagesPipeline': 1
    'taomm.pipelines.JsonWriterPipeline': 100,
    'taomm.pipelines.TaommPipeline': 200

}
# 下载图片存储位置
IMAGES_STORE = 'e:\\PythonCode\\taomm\\taomm\\images'
