from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pymongo
import scrape_mars
import scrape_m_hemis

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.mars_db
db.updates.insert_one({'test': 'test'})
db.hemispheres.insert_one({'test': 'test'})

@app.route("/")
def index():
    updates = db.updates.find()
    hemis = db.hemispheres.find()
    print(updates)
    print(hemis[0])
    return render_template('index.html', updates = updates, hemis = hemis)

@app.route("/scrape")
def scraper():
    scrape_mars.all_the_mars_scrapes()
    scrape_m_hemis.hemi_scrapes()
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)