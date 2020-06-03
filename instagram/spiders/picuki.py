# -*- coding: utf-8 -*-
import scrapy


class PicukiSpider(scrapy.Spider):
    name = 'picuki'
    allowed_domains = ['picuki.com']
    start_urls = ['https://www.picuki.com/profile/nike']

    def parse(self, response):
        posts = response.xpath('//div[@class="box-photo"]')
        for post in posts:
            img_url = post.xpath('.//div//img[@class="post-image"]/@src').get()
            caption = post.xpath('.//div[@class="photo-description"]/text()').get()
            url = post.xpath('.//div[@class="photo"]/a/@href').get()

            yield scrapy.Request(url,
                                 callback=self.parse_post,
                                 meta={'img_url': img_url,
                                       'caption': caption,
                                       'url': url})

    def parse_post(self, response):
        img_url = response.meta['img_url']
        caption = response.meta['caption']

        url = response.meta['url']

        comments = response.xpath('//div[@id="commantsPlace"]/text()')
        for i in range(0, 24):
            likes = response.xpath('.//span[@class="icon-thumbs-up-alt"]/text()').get()
            # need to put a regex here to get just the number value:
            num_of_comments = response.xpath('.//span[@id="commentsCount"]/text()').get()

            comment_user_name = response.xpath('.//*[@class="comment-user-nickname"]/a/text()').get()
            comment_text = response.xpath('.//*[@class="comment-text"]/text()').get()

            yield {'img_url': img_url,
                   'caption': caption,
                   'url': url,
                   'likes': likes,
                   'num_of_comments': num_of_comments,
                   'comment_user_name': comment_user_name,
                   'comment_text': comment_text}





