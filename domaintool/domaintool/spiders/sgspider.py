# -*- coding: UTF-8 -*-
import scrapy
import sys
from scrapy.http import Request
from urllib import unquote
from domaintool.items import DomaintoolItem

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

class SGSpider(scrapy.Spider):
	name='sgspider'
	allowed_domains=['pinyin.sogou.com']
	start_urls=[
		'http://pinyin.sogou.com/dict/cate/index/360',
		'http://pinyin.sogou.com/dict/cate/index/1',
		'http://pinyin.sogou.com/dict/cate/index/76',
		'http://pinyin.sogou.com/dict/cate/index/96',
		'http://pinyin.sogou.com/dict/cate/index/127',
		'http://pinyin.sogou.com/dict/cate/index/132',
		'http://pinyin.sogou.com/dict/cate/index/436',
		'http://pinyin.sogou.com/dict/cate/index/154',
		'http://pinyin.sogou.com/dict/cate/index/389',
		'http://pinyin.sogou.com/dict/cate/index/367',
		'http://pinyin.sogou.com/dict/cate/index/31',
		'http://pinyin.sogou.com/dict/cate/index/403',
]

	def __init__(self):
		self.base_path='/home/ubuntu/sg/'
		self.base_url='http://pinyin.sogou.com'

	def parse(self, response):
		for a in response.xpath('//div[@class="dict_dl_btn"]/a/@href').extract():
#			i=DomaintoolItem()
#			i['url']=a
#			i['path']=self.base_path+unquote(a.split('name=')[1])+'.scel'
			yield Request(a, callback=self.save_scel)
		
		the_last=response.xpath('//div[@id="dict_page_list"]/ul/li[last()]/span/a[@class="now_page"]')	
		if len(the_last) <=0:
			next_page=self.base_url+response.xpath(u'//div[@id="dict_page_list"]/ul/li/span/a[text()="下一页"]/@href').extract()[0]
			print next_page
			yield Request(next_page, callback=self.parse)
		else:
			print '+++++++++++++++++++++++++'
		
	def save_scel(self, response):
		#print response.url
	#	print unquote(response.url.split('name=')[1])
		file=self.base_path+unquote(response.url.split('name=')[1])+'.scel'
		self.logger.error(file)
		with open(file, 'wb') as f:
			f.write(response.body)
