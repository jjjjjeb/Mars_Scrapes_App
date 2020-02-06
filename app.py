from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/craigslist_app")

@app.route("/")
def index():
    updates = mongo.db.updates.find()
    hemispheres = mongo.db.hemispheres.find()
    return render_template('index.html', updates = updates, hemispheres = hemispheres)


@app.route("/scrape")
def scraper():
    updates = mongo.db.updates
    hemispheres = mongo.db.hemispheres
    updates.update({}, scrape_mars.all_the_mars_scrapes(), upsert=True )
    hemispheres.update({}, scrape_mars.hemi_scrapes(), upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
