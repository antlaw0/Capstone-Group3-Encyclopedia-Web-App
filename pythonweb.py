from flickrapi import FlickrAPI

from flask import Flask, render_template, request
import os
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    searchText = None
    flickrImage = None
    flickrImage2 = None
    if request.method == 'POST' and 'searchText' in request.form:
        searchText = request.form['searchText']
        FLICKR_PUBLIC =  os.environ['FLICKR_PUBLIC']
        FLICKR_SECRET =  os.environ['FLICKR_SECRET']
        flickr = FlickrAPI(FLICKR_PUBLIC, FLICKR_SECRET, format='parsed-json')
        extras = 'url_c,url_l,url_o'
        results = flickr.photos.search(text=searchText, per_page=5, extras=extras)
        flickrImage = results['photos']['photo'][0]['url_c']
        flickrImage2 = results['photos']['photo'][1]['url_c']

    return render_template('index.html', flickrImage=flickrImage, flickrImage2=flickrImage2)


if __name__ == '__main__':
    app.run(debug=True)
