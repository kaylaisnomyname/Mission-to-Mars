# s10.5.1 use Flase to create web app : Error 
# need to double check the app1.py and scraping1.py
# checked. worked Nov 6.

# imports
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping   # use scraping code to convert from jupyter notebook to python

app = Flask(__name__)

# tell Python how to connect to mongo using PyMongo
# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# set up app routes
# homepage
@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

# the scraping route at button of the web app
@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_data = scraping.scrape_all()
    mars.update({}, mars_data, upsert=True)
    return redirect('/', code=302)


# tell the app to run
if __name__ == "__main__":
    app.run()


