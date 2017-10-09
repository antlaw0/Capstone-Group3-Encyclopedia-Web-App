from flickrapi import FlickrAPI
import wikipedia
from flask import Flask, render_template, flash, session, redirect, request, url_for
import models as dbHandler
import os
import tweepy
app = Flask(__name__)
from Results import get_result


@app.route('/', methods=['GET', 'POST'])
def index():

    if 'username' in session:
        return redirect(url_for('results'))
    else:
        message=None
        if request.method=='POST':
            username = request.form['username']
            password = request.form['password']
            #if entered username exists
            if dbHandler.userExists(username) == True:
                #if password matches password in database
                if dbHandler.getPassword(username) == password:
                    session['username'] = username
                    return redirect(url_for('results'))

                else:
                    message="Invalid password"
                    return render_template('index.html', message=message)

            else:
                message="User does not exist"
                return render_template('index.html', message=message)

        else:
           return render_template('index.html', message=message)
	
@app.route('/registration', methods=['GET', 'POST'])
def registration():
    message=None
    #find a way to render results without using all these variables here
    wikiText=None
    twitterText=None
    searchText=None
    flickrImage=None
    flickrImage2=None
    wikiImage=None
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        if dbHandler.userExists(username) == True:
            message="UserAlready exists"
            return render_template('registration.html', message=message)
        else:
            #insert new user
            dbHandler.insertUser(username, password)
            return render_template('results.html', flickrImage=flickrImage, flickrImage2=flickrImage2, wikiText=wikiText,
                           wikiImage=wikiImage, searchText=searchText, twitterText=twitterText, username=username)
            
    else:
        return render_template('registration.html', message=message)
    
	
@app.route('/results', methods=['GET', 'POST'])
def results():
    if 'username' in session:
        username = session['username']


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

        return render_template('results.html', flickrImage=flickrImage, flickrImage2=flickrImage2, wikiText=wikiText,
                               wikiImage=wikiImage, searchText=searchText, twitterText=twitterText)
    else:
        return redirect('/')

if __name__ == '__main__':
	app.secret_key = os.urandom(12)
	app.run(debug=True)

