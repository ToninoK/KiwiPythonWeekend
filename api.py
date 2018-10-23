from flask import Flask, jsonify, request, render_template, redirect, url_for

from arriva_scraper import ArrivaScraper
from data_structure import Journey
from db_controller import DbController
from cacheControl import CacheController

APP = Flask(__name__)
arriva = ArrivaScraper()
db = DbController()
db.createTable()
cacher = CacheController()

@APP.route("/")
def red():
    return redirect(url_for('home'))

@APP.route("/home")
def home():
    return render_template('homepage.html')


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


@APP.route("/search", methods=['POST'])
def search():
    source = request.form["source"]
    destination = request.form["destination"]
    date = request.form["date"]
    search = [source, destination, date]
    print("req_mades")
    cached_data = cacher.getJourneys(search)

    if cached_data:
        data = {"journeys": [journey.toDict() for journey in cached_data]}
        return render_template('search.html', data=data)
    data = db.getJourneys(search)
    return render_template('search.html', data=data)

if __name__="__main__":
    APP.run()
