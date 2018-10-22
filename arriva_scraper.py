from requests_html import HTMLSession
from currency_converter import CurrencyConverter
from cacheControl import CacheController, Journey

c = CurrencyConverter()

class ArrivaScraper:
    def __init__(self):
        self.url = "https://www.arriva.com.hr/en-us/choose-your-journey"
        self.session = HTMLSession()
        self.data = {
            "post-type": "shop",
            "currentstepnumber": "1",
            "search-from": None,
            "search-to": None,
            "search-datetime": None,
            "ticket-type": "oneway",
        }
        self.html = None
        self.cacher = CacheController()

    def run(self, source, destination, date):
        search = [source, destination, date]
        self.data["search-from"] = search[0]
        self.data["search-to"] = search[1]
        self.data["search-datetime"] = search[2]

        cached_data = self.cacher.getJourneys(search)

        if cached_data:
            return cached_data

        self.html = self.session.post(self.url, self.data).html

        return self.parseData(search)

    def parseData(self, search):
        dep = self.fetchDepartures()
        arr = self.fetchArrivals()
        dur = self.fetchDurations()
        pr = self.fetchPrices()
        carr = self.fetchCarriers()

        journeys = [
            Journey(
                source=search[0], 
                destination=search[1],
                date=search[2],
                departure=dep[i]+' h',
                arrival=arr[i]+' h',
                duration=dur[i]+' h',
                price=pr[i],
                carrier=carr[i]
            ) for i in range(len(dep))
        ]
        
        return self.cacher.cacheJourneys(journeys, search)

    def fetchDepartures(self):
        return[
            dep.find('strong')[0].text.split('-')[0][:-1] for dep in self.html.find('.vrijeme-top')
        ]
    
    def fetchArrivals(self):
        return[
            arr.find('strong')[0].text.split('-')[1][1:] for arr in self.html.find('.vrijeme-top')
        ]
    
    def fetchPrices(self):
        prices = [ pr.find('a')[0].text.split(',')[0] for pr in self.html.find('.cijena') if pr.find('a') != [] ]
        return[
            round(c.convert( int( ep ),'HRK' ), 2) for ep in prices
        ]
    
    def fetchDurations(self):
        return[
            dur.text[16:] for dur in self.html.find('.vrijeme-bottom')
        ]

    def fetchCarriers(self):
        return[
            carr.text[9:] for carr in self.html.find('.prijevoznik')
        ]
