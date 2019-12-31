import scrapy
from capture.items import MissionItem


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

        name = response.css("span.STYLE2::text").get()

        # filename = '../html/missions/%s.html' % (name if name else "default")
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log('Saved file %s' % filename)

        # For items
        for table in response.css('table'):
            mission_name = table.css("a::attr(name)").get()
            mission_name_2 = table.css("a::text").get()
            sub_table = table.xpath(".//table").get()

            # Is a table and not contains another table
            if mission_name and mission_name == mission_name_2 and not sub_table:
                self.log("Mission found: {}".format(mission_name))

                mission = MissionItem(name=mission_name, location=str(name).split("-")[-1])
                index = 0
                for tr in table.css("tr"):
                    if index == 1:
                        mission["character"] = tr.css("td::text")[-1].get()
                    elif index == 2:
                        mission["limitation"] = tr.css("td::text")[-1].get()
                    elif index == 3:
                        mission["process"] = tr.css("td::text")[-1].get()
                    elif index == 4:
                        mission["reward"] = tr.css("td::text")[-1].get()
                    index += 1
                yield mission
        
        # For requests
        for link in response.css("a"):
            location = link.css("::text").get()
            url = link.css("::attr(href)").get()

            # Not an archor
            if url is not None and "#" not in url:
                next_page = response.urljoin(url)
                yield scrapy.Request(next_page, callback=self.parse)
                # Duplicate filter can do this for us
                # if next_page not in QuotesSpider.visited:
                #    self.log("Will visit next page: {} {}".format(location, next_page))
                #    QuotesSpider.visited.append(next_page)
                #    yield scrapy.Request(next_page, callback=self.parse)
                # else:
                #     self.log("Visited page: {} {}".format(location, next_page))
