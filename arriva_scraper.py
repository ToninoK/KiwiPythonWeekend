from requests_html import HTMLSession


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

    def run(self, source, destination, date):
        self.data["search-from"] = source
        self.data["search-to"] = destination
        self.data["search-datetime"] = date

        return self.fetch_departures(self.get_html())           

    def get_html(self):
        res = session.post(self.url, self.data)
        return res.html

    def fetch_departures(self, html_data):
        return[
            dep.find('strong').text for dep in html_data.find('.vrijeme-top')
        ]
    
    def fetch_departures(self, html)