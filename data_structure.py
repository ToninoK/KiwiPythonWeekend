from dataclasses import dataclass


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
