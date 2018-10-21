from requests_html import HTMLSession
from currency_converter import CurrencyConverter
from dataclasses import dataclass

c = CurrencyConverter()

@dataclass
class Journey:
    source:str = None
    destination:str = None
    date:str = None
    departure:str = None
    arrival:str = None
    duration:str = None
    price:float = None
    carrier:str = None

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

    def run(self, source, destination, date):
        search = [source, destination, date]
        self.data["search-from"] = search[0]
        self.data["search-to"] = search[1]
        self.data["search-datetime"] = search[2]

        self.html = self.session.post(self.url, self.data).html

        return self.parse_data(search)

    def parse_data(self, search):
        dep = self.fetch_departures()
        arr = self.fetch_arrivals()
        dur = self.fetch_duration()
        pr = self.fetch_prices()
        carr = self.fetch_carrier()

        return [
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

    def fetch_departures(self):
        return[
            dep.find('strong')[0].text.split('-')[0][:-1] for dep in self.html.find('.vrijeme-top')
        ]
    
    def fetch_arrivals(self):
        return[
            arr.find('strong')[0].text.split('-')[1][1:] for arr in self.html.find('.vrijeme-top')
        ]
    
    def fetch_prices(self):
        prices = [ pr.find('a')[0].text.split(',')[0] for pr in self.html.find('.cijena') if pr.find('a') != [] ]
        return[
            round(c.convert( int( ep ),'HRK' ), 2) for ep in prices
        ]
    
    def fetch_duration(self):
        return[
            dur.text[16:] for dur in self.html.find('.vrijeme-bottom')
        ]

    def fetch_carrier(self):
        return[
            carr.text[9:] for carr in self.html.find('.prijevoznik')
        ]
