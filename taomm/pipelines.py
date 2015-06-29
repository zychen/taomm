# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import hashlib
import json
import os

from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.http import Request
from taomm import settings


class TaommPipeline(ImagesPipeline):
    """保存图片"""
    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            image_path = item['nickname'] + '/' + item['nickname'] + '_'
            yield Request(image_url, meta={'image_path': image_path})

    def file_path(self, request, response=None, info=None):
        ## start of deprecation warning block (can be removed in the future)
        def _warn():
            from scrapy.exceptions import ScrapyDeprecationWarning
            import warnings
            warnings.warn('ImagesPipeline.image_key(url) and file_key(url) methods are deprecated, '
                          'please use file_path(request, response=None, info=None) instead',
                          category=ScrapyDeprecationWarning, stacklevel=1)

        # check if called from image_key or file_key with url as first argument
        if not isinstance(request, Request):
            _warn()
            url = request
        else:
            url = request.url

        # detect if file_key() or image_key() methods have been overridden
        if not hasattr(self.file_key, '_base'):
            _warn()
            return self.file_key(url)
        elif not hasattr(self.image_key, '_base'):
            _warn()
            return self.image_key(url)
        ## end of deprecation warning block

        # 在图片guid前添加TaoMM昵称，并且每个昵称一个文件夹
        image_path = request.meta['image_path']
        image_guid = hashlib.md5(url).hexdigest()  # change to request.url after deprecation
        return '%s_%s.jpg' % (image_path, image_guid)


class JsonWriterPipeline(object):
    def __init__(self):
        self.basedir = os.path.abspath(settings.IMAGES_STORE)

    def process_item(self, item, spider):
        jsonname = item['nickname'] + '/' + item['nickname'] + '_info.json'
        json_absolute_path = self._get_filesystem_path(jsonname)
        self._mkdir(json_absolute_path)

        txtname = item['nickname'] + '/' + item['nickname'] + '_info.txt'
        txt_absolute_path = self._get_filesystem_path(txtname)
        self._mkdir(txt_absolute_path)

        info = item['detail']
        with open(txt_absolute_path, 'w') as fw:
            fw.write(info)

        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        with open(json_absolute_path, 'w') as fw:
            fw.write(line)

        return item

    def _get_filesystem_path(self, path):
        path_comps = path.split('/')
        return os.path.join(self.basedir, *path_comps)

    def _mkdir(self, path):
        dirname = os.path.dirname(path)

        if not os.path.exists(dirname):
            os.makedirs(dirname)







