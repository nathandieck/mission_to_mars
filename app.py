from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/craigslist_app"
mongo = PyMongo(app)

@app.route("/")
def index():
    go2mars = mongo.db.go2mars.find_one()
    return render_template("index.html", go2mars=go2mars)

@app.route("/scrape") 
def scraper():
    go2mars = mongo.db.go2mars
    go2mars_data = scrape_mars.scrape()
    go2mars.update({}, go2mars_data, upsert = True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)