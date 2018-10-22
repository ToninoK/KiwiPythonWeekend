from redis import Redis
from slugify import slugify
import json

from data_structure import Journey

host = "127.0.0.1"
port = 3001


class CacheController:
    def __init__(self):
        self.red = Redis(host=host, port=port)

    def createName(self, search_data):
        return slugify(
            f"journey:{search_data[0]}_{search_data[1]}_{search_data[2]}:tonino"
        )

    def cacheJourneys(self, journeys, search_data):
        journeys_name = self.createName(search_data)
        self.red.setex(
            journeys_name,
            json.dumps({"journeys": [journey.toDict() for journey in journeys]}),
            60 * 60,
        )
        return journeys

    def getJourneys(self, search_data):
        journeys_name = self.createName(search_data)
        journeys = self.red.get(journeys_name)
        if journeys:
            return [
                Journey(
                    source=journey["source"],
                    destination=journey["destination"],
                    date=journey["date"],
                    departure=journey["departure"],
                    arrival=journey["arrival"],
                    duration=journey["duration"],
                    price=journey["price"],
                    carrier=journey["carrier"],
                )
                for journey in dict(json.loads(journeys))["journeys"]
            ]
        return False
