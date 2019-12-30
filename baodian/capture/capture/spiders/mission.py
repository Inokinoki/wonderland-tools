import scrapy


class MissionSpider(scrapy.Spider):
    name = "mission"
    # visited = []

    def start_requests(self):
        urls = [
            'http://www.wangjiuyue.cn/plhj/rwzl/20060420/185206.html',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-1]
        filename = '../html/missions/%s' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
        for link in response.css("a"):
            location = link.css("::text").get()
            url = link.css("::attr(href)").get()

            # Not an archor
            if url is not None and "#" not in url:
                next_page = response.urljoin(url)
                # Duplicate filter can do this for us
                # if next_page not in QuotesSpider.visited:
                #    self.log("Will visit next page: {} {}".format(location, next_page))
                #    QuotesSpider.visited.append(next_page)
                yield scrapy.Request(next_page, callback=self.parse)
                # else:
                #     self.log("Visited page: {} {}".format(location, next_page))