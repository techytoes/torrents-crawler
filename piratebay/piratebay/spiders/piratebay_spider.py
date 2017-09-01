from scrapy.spiders import BaseSpider
from scrapy import Selector

import urllib
import cfscrape
from urllib.parse import urlparse

from piratebay.items import UniversalItem

#Spider for PirateBay
class PiratebaySpider(BaseSpider):
    name = "piratebay"
    with open('links/piratebay.txt', 'r') as file:
        start_urls = [i.strip() for i in file.readlines()]

    def parse(self, response):
        hxs = Selector(response)
        sites = hxs.xpath('//div[@class="detName"]')
        for site in sites:
            item = UniversalItem()
            item['title'] = site.xpath('a/text()').extract()[0]
            item['link'] = "http://thepiratebay.org" + site.xpath('a/@href').extract()[0]
            item['ref'] = "thepiratebay.org"
            yield item

#Spider for Leetx
class LeetxSpider(BaseSpider):
    name = "leetx"
    allowed_domains = ["1337x.to"]
    with open('links/leetx.txt', 'r') as file:
        start_urls = [i.strip() for i in file.readlines()]

    def parse(self, response):
        hxs = Selector(response)
        sites = hxs.xpath('//h3[@class="to"]')
        for site in sites:
            item = UniversalItem()
            item['title'] = site.xpath('a/text()').extract()[0]
            item['link'] = "https://1337x.to" + site.xpath('a/@href').extract()[0]
            item['ref'] = "1337x.to"
            yield item

#Spider for SkidrowCrack
class SkidrowCrackSpider(BaseSpider):
    name = "skidrowcrack"
    allowed_domains = ["skidrowcrack.com"]
    with open('links/skidrowcrack.txt', 'r') as file:
        start_urls = [i.strip() for i in file.readlines()]

    def parse(self, response):
        hxs = Selector(response)
        sites = hxs.xpath('//ul[@class="lcp_catlist"]/li')
        for site in sites:
            item = UniversalItem()
            item['title'] = site.xpath('a/text()').extract()[0]
            item['link'] = site.xpath('a/@href').extract()[0]
            item['ref'] = "skidrowcrack.com"
            yield item

#Spider for TorrentDownload
class TorrentDownloadsSpider(BaseSpider):
    name = "torrentdownloads"
    allowed_domains = ["torrentdownloads.me"]
    with open('links/torrentdownloads.txt', 'r') as file:
        start_urls = [i.strip() for i in file.readlines()]

    def parse(self, response):
        hxs = Selector(response)
        titles = hxs.xpath('//div[@class="inner_container"]/div/p/a/text()').extract()
        links = hxs.xpath('//div[@class="inner_container"]/div/p/a/@href').extract()
        for i, v in zip(titles,links):
            item = UniversalItem()
            item['title'] = i
            item['link'] = "http://www.torrentdownloads.me" + v
            item['ref'] = "torrentdownloads.me"
            yield item

#Spider for SumoTorrent
class SumoTorrentSpider(BaseSpider):
    name = "sumotorrent"
    allowed_domains = ["sumotorrent.sx"]
    with open('links/sumotorrent.txt', 'r') as file:
        start_urls = [i.strip() for i in file.readlines()]

    def parse(self, response):
        hxs = Selector(response)
        sites = hxs.xpath('//div[@style="overflow:hidden;width:95%;height:15px;padding-top:4px;padding-bottom:4px;white-space: nowrap;"]')
        for site in sites:
            item = UniversalItem()
            item['title'] = site.xpath('a/text()').extract()[0]
            item['link'] = url_fix(site.xpath('a/@href').extract()[0])
            item['ref'] = "sumotorrent.sx"
            yield item

#Spider for Bitsnoop
class BitSnoopSpider(BaseSpider):
    name = "bitsnoop"
    allowed_domains = ["bitsnoop.com"]
    start_urls = ["http://bitsnoop.com/popular/seeders_games.html"]

    def parse(self, response):
        hxs = Selector(response)
        sites = hxs.xpath('//ol[@id="torrents"]/li')
        for site in sites:
            item = UniversalItem()
            item['title'] = site.xpath('a/text()').extract()[0]
            item['link'] = "http://bitsnoop.com" + url_fix(site.xpath('a/@href').extract()[0])
            item['ref'] = "bitsnoop.com"
            yield item

#spider for bitsnoop
class bitsnoop(BaseSpider):
    name = "bitsnoop2"
    allowed_domains = ["bitsnoop.mobi"]
    with open('links/bitsnoop.txt', 'r') as file:
        start_urls = [i.strip() for i in file.readlines()]

    def parse(self, response):
        hxs = Selector(response)
        sites = hxs.xpath('//div[@class="detName"]')
        for site in sites:
            item = UniversalItem()
            item['title'] = site.xpath('a/text()').extract()[0]
            item['link'] = "http://bitsnoop.mobi" + site.xpath('a/@href').extract()[0]
            item['ref'] = "bitsnoop.mobi"
            yield item

class btetree(BaseSpider):
    name = "btetree"
    allowed_domains = ["bt.etree.org"]
    with open('links/btetree.txt', 'r') as file:
        start_urls = [i.strip() for i in file.readlines()]

    def parse(self, response):
        for response in response.css("a.details_link"):
            yield{
                'text' : response.css("b::text").extract_first()
            }

class gameUpdates(BaseSpider):
    name = "gameup"
    allowed_domains = ["http://gameupdates,org"]
    with open('links/gameup.txt', 'r') as file:
        start_urls = [i.strip() for i in file.readlines()]

    def parse(self, response):
        for response in response.css("div.textBox table.niceBox"):
            yield{
                'text' : response.css("tr td a.index::attr(title)").extract_first()
            }

class mediaccc(BaseSpider):
    name = "mediaccc"
    allowed_domains = ["https://media.ccc.de/"]
    with open('links/mediaccc.txt', 'r') as file:
        start_urls = [i.strip() for i in file.readlines()]
    
    def parse(self, response):
        for response in response.css("div.caption"):
            yield{
                'text' : response.css("h3 a::text").extract_first()
            }

def url_fix(s, charset='utf-8'):
    if isinstance(s, unicode):
        s = s.encode(charset, 'ignore')
    scheme, netloc, path, qs, anchor = urlparse.urlsplit(s)
    path = urllib.quote(path, '/%')
    qs = urllib.quote_plus(qs, ':&=')
    return urlparse.urlunsplit((scheme, netloc, path, qs, anchor))
