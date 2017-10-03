from flickrapi import FlickrAPI
import wikipedia
from flask import Flask, render_template, request
import os
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    searchText=None
    wikiImage = None
    wikiText = None
    flickrImage = None
    flickrImage2 = None
    
    if request.method == 'POST' and 'searchText' in request.form:
        searchText = request.form['searchText']
    
        wikiPage = wikipedia.page(searchText)
        wikiText = wikiPage.content
        wikiImage = wikiPage.images[0]
        
	
        FLICKR_PUBLIC =  '2996c5433c7c633978adb98583ac21fd'#os.environ['FLICKR_PUBLIC']
        FLICKR_SECRET =  'Ydbfbfec07e8f9c22'#os.environ['FLICKR_SECRET']
        flickr = FlickrAPI(FLICKR_PUBLIC, FLICKR_SECRET, format='parsed-json')
        extras = 'url_c,url_l,url_o'
        results = flickr.photos.getRecent(text=searchText, per_page=5, extras=extras)
        flickrImage = results['photos']['photo'][0]['url_l']
        flickrImage2 = results['photos']['photo'][1]['url_l']
    
    return render_template('index.html', flickrImage=flickrImage, flickrImage2=flickrImage2, wikiText=wikiText, wikiImage=wikiImage, searchText=searchText)

        

if __name__ == '__main__':
    app.run(debug=True)