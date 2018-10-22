from dataclasses import dataclass

create_table = """ 
    CREATE TABLE IF NOT EXISTS journeys_tonino(
    -- id SERIAL PRIMARY KEY,
   source TEXT,
   destination TEXT,
   date TEXT,
   departure TEXT,
   arrival TEXT,
   duration TEXT,
   price FLOAT,
   carrier TEXT
); """

insert_table = """
    INSERT INTO journeys_tonino (source, destination, date, departure, arrival, duration, price, carrier)
    VALUES (%(source)s,
            %(destination)s,
            %(date)s,
		    %(departure)s,
            %(arrival)s,
            %(duration)s,
            %(price)s,
            %(carrier)s
);"""

drop_table = """DROP TABLE IF EXISTS journeys_tonino"""

select_tables = """SELECT * FROM journeys_Tonino WHERE source = %(source)s AND destination = %(destination)s AND date = %(date)s"""


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


def toJourney(journey):
    return Journey(
        source=journey["source"],
        destination=journey["destination"],
        date=journey["date"],
        departure=journey["departure"],
        arrival=journey["arrival"],
        duration=journey["duration"],
        price=journey["price"],
        carrier=journey["carrier"],
    )
