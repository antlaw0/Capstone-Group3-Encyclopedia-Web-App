from flickrapi import FlickrAPI
import wikipedia
from flask import Flask, render_template, flash, session, redirect, request, url_for
import models as dbHandler
import os
import datetime
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
                    return redirect(url_for('user'))

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

    message = None
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        if dbHandler.userExists(username) == True:
            message="UserAlready exists"
            return render_template('registration.html', message=message)
        else:
            #insert new user
            dbHandler.insertUser(username, password)
            session['username'] = username
            return redirect(url_for('user'))
    else:
        return render_template('registration.html', message=message)
    
	
@app.route('/results', methods=['GET', 'POST'])
def results():
    if 'username' in session:
        username = session['username']
        searchText = None
        wikiImage = None
        wikiText = None
        twitterText = None
        photos = []
        if request.method == 'POST' and 'searchText' in request.form:
            searchText = request.form['searchText']
            raw_flickr_text,raw_flickr_images = get_result("flickr", searchText)
            for index in range (len(raw_flickr_images)):
                if index == 25:
                    break
                flickrImage = raw_flickr_images[index]
                photos.append(flickrImage)
            print((photos[0]))
            wikiText,raw_wiki_images = get_result("wikipedia", searchText)
            wikiImage = raw_wiki_images[0]

            twitterText,raw_twitter_images = get_result("twitter", searchText)

        return render_template('results.html', flickrImageList = photos, wikiText=wikiText,
                               wikiImage=wikiImage, searchText=searchText, twitterText=twitterText, username=username)
    else:
        return redirect('/')
@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('username', None)
   return redirect(url_for('index'))

@app.route('/user')
def user():
    if 'username' in session:
        username=session['username']
        searchList=dbHandler.showSearches(username)    
        return render_template('userHome.html', searchList=searchList)
    else:
        return render_template('index.html', message=None)
@app.route('/save', methods=['POST'])
def saveSearch():
    searchText = request.form['searchText']
    date = datetime.datetime.now()
    username = session['username']
    dbHandler.createSearch(username, searchText, date)
    return redirect(url_for('results'))
@app.route('/deleate')
def deleateSearches():
    username = session['username']
    dbHandler.deleateSearches(username)
    return redirect(url_for('results'))

if __name__ == '__main__':
	app.secret_key = os.urandom(12)
	app.run(debug=True)
