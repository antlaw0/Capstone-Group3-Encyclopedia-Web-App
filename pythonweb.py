from flickrapi import FlickrAPI
import wikipedia
from flask import Flask, render_template, request
import os
import tweepy
app = Flask(__name__)
from Results import get_result


@app.route('/', methods=['GET', 'POST'])
def index():
    searchText = None
    wikiImage = None
    wikiText = None
    flickrImage = None
    flickrImage2 = None
    twitterText = None

    if request.method == 'POST' and 'searchText' in request.form:
        searchText = request.form['searchText']

        raw_flickr_text,raw_flickr_images = get_result("flickr", searchText)
        flickrImage = raw_flickr_images[0]
        flickrImage2 = raw_flickr_images[1]

        wikiText,raw_wiki_images = get_result("wikipedia", searchText)
        wikiImage = raw_wiki_images[0]

        twitterText,raw_twitter_images = get_result("twitter", searchText)

    return render_template('index.html', flickrImage=flickrImage, flickrImage2=flickrImage2, wikiText=wikiText,
                           wikiImage=wikiImage, searchText=searchText, twitterText=twitterText)


if __name__ == '__main__':
    app.run(debug=True)