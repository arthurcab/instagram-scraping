from scrapy import Spider
from scrapy.http import Request


class ClasscentralSpider(Spider):
    name = 'classcentral'
    allowed_domains = ['classcentral.com']
    start_urls = ['https://www.classcentral.com/subjects']

    def __init__(self, subject=None):
        self.subject = subject

    def parse(self, response):
        if self.subject:
            subject_url = response.xpath(f'//a[contains(@title, "{self.subject}")]/@href').get()
            absolute_subject_url = response.urljoin(subject_url)
            yield Request(absolute_subject_url,
                          callback=self.parse_subject)
        else:
            self.log('Scraping all subjects')
            subjects = response.xpath('//h3/a[1]/@href').getall()
            for subject in subjects:
                absolute_subject_url = response.urljoin(subject)
                yield Request(absolute_subject_url,
                              callback=self.parse_subject)

    def parse_subject(self, response):
        subject_name = response.xpath('//h1/text()').get()
        courses = response.xpath('//tr[@itemtype="http://schema.org/Event"]')
        for course in courses:
            # remove the new line character and strip the whitespace
            course_name = course.xpath('.//*[@itemprop="name"]/text()').get().replace('\n', '').strip()
            course_url = course.xpath('.//a[@itemprop="url"]/@href').get()
            absolute_course_url = response.urljoin(course_url)
            school = course.xpath('//a[@class="color-charcoal small-down-text-2 text-3"]/text()').get().replace('\n', '').strip()
            school_url = course.xpath('.//a[@class="color-charcoal small-down-text-2 text-3"]/@href').get()
            school_absolute_url = response.urljoin(school_url)
            start_date = course.xpath('.//td[3]/text()').get().replace('\n', '').strip()

            yield {'course_name': course_name,
                   'absolute_course_url': absolute_course_url,
                   'school': school,
                   'school_absolute_url': school_absolute_url,
                   'subject_name': subject_name,
                   'start_date': start_date}
        next_page = response.xpath('//link[@rel="next"]/@href').get()
        if next_page:
            absolute_next_page = response.urljoin(next_page)

            yield Request(absolute_next_page,
                          callback=self.parse_subject)

