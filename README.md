# Zapier App Recommender

This is a prototype of a website to recommend end-users, sales, or support folks to figure out what types of app are available on the Zapier platform (of which there are many), based on text descriptions of apps versus a tag-based system which is a generally more scalable way to search for things.

A prototype is available [on Heroku](https://arcane-shelf-86847.herokuapp.com/
). Feel free to try it out!

The system is built off of Elasticsearch and scraping the Zapier site (sorry!)

## Running locally

If you'd like to try and roll it out on your own, ideally you'll need:

* venv
* an Elasticsearch host (that has an index of `/zap/apps`)
* Heroku

To set up the environment:
```
pip install -r requirements.txt
```

To run the scraper:
```
python ./zapapp/data/scraper.py
```

To upload your docs to a local Elasticsearch cluster (or try out [Bonsai](https://bonsai.io)!), which is needed for this app to run:
```
python ./zapapp/data/elastic_upload.py
```

To run the web app (all scraped data exists in this repo):
```
python ./zapapp/app.py $PORT $ES_URL
```

