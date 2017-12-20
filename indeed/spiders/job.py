import scrapy
from indeed.items import IndeedItem


class job(scrapy.Spider):
    def url_creater(keyword, city, state, pages = 1):
        keyword = keyword.strip().replace(' ','+')
        city = city.strip().replace(' ','+')
        state = state.strip()
        url_list = []
        base_url = 'https://www.indeed.com/jobs?q='+keyword+'&l='+city+'%2C+'+state+'&start='
        url = base_url + str(pages*10)
        url_list.append(url)
        return url_list

    name = "indeed"
    allowed_domains = ["indeed.com"]
    start_urls = url_creater('data analyst','Champaign','IL',1)
    
    
    def parse(self, response):
        list = response.xpath("//div[contains(@class,'row')]")

        for row in list:
            title = row.xpath("//a[@data-tn-element='jobTitle']/@title").extract()
            companyina = row.xpath("//span[@class='company']/a/text()").extract()
            companynoa = row.xpath("//span[@class='company']/text()").extract()
            location = row.xpath("//span[@class='location']/text()").extract()
            
            ka = 0
            kn = 0
            for kn in range(len(companynoa)):
                if companynoa[kn] == '\n    ':
                    companynoa[kn] = companyina[ka].strip('    \n')
                    ka += 1
                else:
                    companynoa[kn] = companynoa[ka].strip('    \n')
                kn += 1
            company = companynoa
            
            item = IndeedItem()
            item['title'] = title
            item['company'] = company
            item['location'] = location
            
        yield item

