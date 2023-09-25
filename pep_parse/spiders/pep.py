import re
import scrapy


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        """Метод, загружающий и обрабатывающий ссылки на документы PEP."""
        numerical_index = response.css('section#numerical-index')
        tbody = numerical_index.css('tbody')
        for tr in tbody.css('tr'):
            pep_href = tr.css('a').attrib['href']
            pep_link = response.urljoin(pep_href) + '/'

            yield response.follow(
                pep_link,
                callback=self.parse_pep,
            )

    def parse_pep(self, response):
        """Метод, обрабатывающий страницу конкретного PEP."""
        h1_tag = response.css('h1.page-title::text').get()
        pattern = r'^PEP\s*?(?P<number>\d+)\s*–\s*(?P<name>.*)$'
        pep_match = re.search(pattern, h1_tag)
        number, name = pep_match.group('number'), pep_match.group('name')

        status_tag = response.css('dt.field-even + dd').get()
        pattern_status = r'.*?<abbr[^>]*>(?P<status>[^>]+)<\/abbr>'
        status_match = re.search(pattern_status, status_tag)
        status = status_match.group('status')

        yield {
            'number': number,
            'name': name,
            'status': status
        }
