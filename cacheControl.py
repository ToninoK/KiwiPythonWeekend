from redis import Redis
from slugify import slugify
from dataclasses import dataclass
import json

host = "127.0.0.1"
port = 3001


@dataclass
class Journey:
    source: str = None
    destination: str = None
    date: str = None
    departure: str = None
    arrival: str = None
    duration: str = None
    price: float = None
    carrier: str = None

    def toDict(self):
        return {
            "source": self.source,
            "destination": self.destination,
            "date": self.date,
            "departure": self.departure,
            "arrival": self.arrival,
            "duration": self.duration,
            "price": self.price,
            "carrier": self.carrier,
        }


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
