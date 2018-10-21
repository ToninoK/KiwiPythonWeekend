from requests_html import HTMLSession


class ArrivaScraper:
    def __init__(self):
        self.url = "https://www.arriva.com.hr/en-us/choose-your-journey"
        self.session = HTMLSession()
        self.data = {
            "post-type": "shop",
            "currentstepnumber": "1",
            "search-from": source,
            "search-to": dest,
            "search-datetime": date,
            "ticket-type": "oneway",
        }

    def get_html(self):
        res = session.post(self.url, self.data)

        return res.html
