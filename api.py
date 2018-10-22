from flask import Flask, jsonify, request

from arriva_scraper import ArrivaScraper
from data_structure import Journey
from db_controller import DbController
from cacheControl import CacheController

APP = Flask(__name__)
arriva = ArrivaScraper()
db = DbController()
db.createTable()
cacher = CacheController()


@APP.route("/test")
def test():
    return "<h1>Test</h1>"


@APP.route("/add")
def add():
    source = request.args.get("source")
    destination = request.args.get("dest")
    date = request.args.get("date")
    search = [source, destination, date]
    data = arriva.run(search[0], search[1], search[2])
    lst_of_journeys = [journey.toDict() for journey in data]
    db.saveJourneys(lst_of_journeys)
    return jsonify({"journeys": lst_of_journeys})


@APP.route("/")
def get_journeys():
    source = request.args.get("source")
    destination = request.args.get("dest")
    date = request.args.get("date")
    search = [source, destination, date]

    cached_data = cacher.getJourneys(search)

    if cached_data:
        return jsonify({"journeys": [journey.toDict() for journey in cached_data]})

    data = db.getJourneys(search)
    return jsonify(data)
