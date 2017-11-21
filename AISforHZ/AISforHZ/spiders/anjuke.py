import scrapy
from AISforHZ.items import AddressItem, CommunityItem 

COUNTRY = ''
PROVINCE = ''
CITY = ''

class anjuke(scrapy.Spider):
    name = 'anjuke'
    start_urls = ['https://hz.fang.anjuke.com/loupan/?from=navigation',
                  'https://hangzhou.anjuke.com/community/?from=navigation']

    def parse(self, response):
        # community type get
        logo = response.css('.site-logo>.xf-logo::text').extract()
        #distinct_new = {}
        #distinct_old = {}
        # new community
        if logo:
            # get the url of distinct
            contents = response.css('.filter>a').extract()
            for content in contents:
                if 'subway' in content:
                    continue
                name = content.split('>')[1].split('<')[0].strip()
                url  = content.split('"')[1]
                #distinct_new[name] = url
                req = scrapy.Request(url, callback=self.parse_distinct)
                req.meta['distinct'] = name
                req.meta['logo'] = logo
                yield req
        # old community
        else: 
            contents = response.css('.elems-l>a').extract()
            for content in contents:
                if not url.startswith('<a href') or 'selected-item' in url:
                    continue
                name = content.split('>')[1].split('<')[0].strip()
                url  = content.split('"')[1]
                #distinct_new[name] = url
                req = scrapy.Request(url, callback=self.parse_distinct)
                req.meta['distinct'] = name
                req.meta['logo'] = logo
                yield req

    def parse_distinct(self, response):
        logo = response.meta['logo']
        distinct = response.meta['distinct']
        
        if logo:
            contents = response.css('.filter-sub>a').extract()
        else:
            contents = response.css('.sub-items>a').extract()
            
        for content in contents:
            if 'selected-item' in content:
                continue
            name = content.split('>')[1].split('<')[0].strip()
            url  = content.split('"')[1]
            req = scrapy.Request(url, callback=self.parse_area)
            req.meta['distinct'] = distinct
            req.meta['area'] = name
            req.meta['logo'] = logo
            yield req
            
    def parse_area(self, response):
        logo = response.meta['logo']
        distinct = response.meta['distinct']
        area = response.meta['area']
        
        if logo:
            urls = response.css('a.lp-name::attr(href)').extract()
            for url in urls:
                fields = url.split('/')
                fields[-1] = 'canshu-' + fields[-1]
                url = '/'.join(fields)
                req = scrapy.Request(url, callback=self.parse_comm_page)
                req.meta['distinct'] = distinct
                req.meta['area'] = area
                req.meta['logo'] = logo
                yield req
            next_page = response.css('.next-page::attr(href)').extract()                       
        else:
            links = response.css('.li-itemmod::attr(link)').extract()
            for link in links:
                url = 'https://hangzhou.anjuke.com'+link
                req = scrapy.Request(url, callback=self.parse_comm_page)
                req.meta['distinct'] = distinct
                req.meta['area'] = area
                req.meta['logo'] = logo
                yield req
            next_page = response.css('.aNxt::attr(href)').extract()
        if not next_page:
            return
        url = next_page[0]
        req = scrapy.Request(url, callback=self.parse_area)
        req.meta['distinct'] = distinct
        req.meta['area'] = area
        req.meta['logo'] = logo
        yield req
        
    def parse_comm_page(self, response):
        addressItem = AddressItem()
        communityItem = CommunityItem()
        comm_info = {}

        logo = response.meta['logo']       
        addressItem['distinct'] = response.meta['distinct']
        addressItem['area'] = response.meta['area']        
        addressItem['city'] = CITY
        addressItem['province'] = PROVINCE
        addressItem['country'] = COUNTRY
        
        if logo:
            lis = response.css('.list>li')
            for li in lis:
                names = li.css('.name::text').extract()
                if names:
                    for name in names:
                        name = name.split(':')[0]
                        des = li.css('.des>a::text').extract()
                        if des:
                            comm_info[name] = [d.strip() for d in des if '[' not in d][0]
                        des = li.css('.des::text').extract()
                        if des:
                            comm_info[name] = [d.strip() for d in des if '[' not in d][0]
            addressItem['address_name'] = comm_info.get(u'楼盘地址', '')
            communityItem['property_mange_fee'] = comm_info.get(u'物业管理费', '')
            communityItem['households'] = comm_info.get(u'规划户数', '')
            communityItem['households_comment'] = ''
            fields = communityItem['households'].split()
            if len(fields) > 1:
                communityItem['households'] = fields[0]
                communityItem['households_comment'] = fields[1]
            communityItem['built_date'] = comm_info.get(u'工程进度', '')
            communityItem['parking_no'] = comm_info.get(u'车位数', '')
        else:
            addrs = response.css('.sub-hd::text').extract()
            addressItem['address_name'] = [addr for addr in addrs if addr][0]
            names = response.css('.comm-title>h1::text').extract()
            communityItem['comm_name'] = [name for name in names if name][0]
            labels = response.css('.basic-parms-mod>dt::text').extract()
            labels = [''.join(label.split('：')[0].split()) for label in labels]
            values = response.css('.basic-parms-mod>dd::text').extract()
            comm_info = dict(zip(labels, values))
            communityItem['property_mange_fee'] = comm_info.get(u'物业费', '')
            communityItem['households'] = comm_info.get(u'总户数', '')
            communityItem['built_date'] = comm_info.get(u'建造年代', '')
            communityItem['parking_no'] = comm_info.get(u'停车位', '')
        communityItem['property_type'] = comm_info.get(u'物业类型', '')
        communityItem['property_name'] = comm_info.get(u'物业公司', '')
        communityItem['building_type'] = comm_info.get(u'建筑类型', '')
        communityItem['comm_area'] = comm_info.get(u'总建面积', '')
        communityItem['parking_rate'] = comm_info.get(u'车位比', '')
        communityItem['capacity_rate'] = comm_info.get(u'容积率', '')
        communityItem['greening_rate'] = comm_info.get(u'绿化率', '')
        communityItem['developer'] = comm_info.get(u'开发商', '')
        communityItem['school'] = comm_info.get(u'相关学校', '')

                    