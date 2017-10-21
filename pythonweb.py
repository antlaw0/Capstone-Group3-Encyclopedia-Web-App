
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

    if 'email' in session:
        return redirect(url_for('results'))
    else:
        message=None
        if request.method=='POST':
            
            email = request.form['email']
            password = request.form['password']
            #if entered email exists
            if dbHandler.userExists(email) == True:
                #if password matches password in database
                if dbHandler.getPassword(email) == password:
                    session['username']=dbHandler.getUsername(email)
                    session['email'] = email
                    return redirect(url_for('user'))

                else:
                    message="Invalid password"
                    return render_template('index.html', message=message)

            else:
                message="User with that e-mail does not exist"
                return render_template('index.html', message=message)

        else:
           return render_template('index.html', message=message)
	
@app.route('/registration', methods=['GET', 'POST'])
def registration():

    messages = []
    
    if request.method=='POST':
        email=request.form['email']
        username = request.form['username']
        password = request.form['password']
		
        #check username length
        if len(username) < 1:
            messages.append("Invallid username")
        if len(username) > 20:
            messages.append("Invallid username- The entered username is too long. Usernames must be 20 characters or less in length.")
        
        #check password length
        if len(password) < 8:
            messages.append("Invallid password- passwords must be at least 8 characters long.")
        if len(password) > 20:
            messages.append("Invallid password- The password you entered is too long. Passwords must not be longer than 20 characters in length.")
        
        #if no error messages
        if len(messages) != 0:
            #return registration page with new error message(s)
            return render_template('registration.html', messages=messages)
        
        if dbHandler.userExists(email) == True:
            messages.append("User with that e-mail already exists")
            return render_template('registration.html', messages=messages)
        else:
            #insert new user
            dbHandler.insertUser(email, username, password)
            session['username'] = username
            session['email']=email
            return redirect(url_for('user'))
    else:
        return render_template('registration.html', messages=messages)
    
	
@app.route('/results', methods=['GET', 'POST'])
def results():
    if 'username' in session:
        username = session['username']
        searchText = None
        wikiImage = None
        searchTerm=None
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
            if len(raw_wiki_images) > 0:
                wikiImage = raw_wiki_images[0]

            twitterText,raw_twitter_images = get_result("twitter", searchText)

        return render_template('results.html', flickrImageList = photos, wikiText=wikiText,
                               wikiImage=wikiImage, searchText=searchText, twitterText=twitterText, username=username, searchTerm=searchTerm)
    else:
        return redirect('/')
@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('username', None)
   session.pop('email', None)
   
   return redirect(url_for('index'))

@app.route('/user', methods=['GET', 'POST'])
def user():
    searchText=None
    searchTerm=None
    photos=[]
    twitterText=None
    flickrImage=None
    wikiImage=None
    wikiText=None
    if 'email' in session:
        username=session['username']
        
        #if clicked search button on previously searched term
        if request.method=='POST':
            searchTerm = request.form['searchTerm'] #get search term from table
            searchText=searchTerm
            #have search term from form, use it in render results page
            raw_flickr_text,raw_flickr_images = get_result("flickr", searchText)
            for index in range (len(raw_flickr_images)):
                if index == 25:
                    break
                flickrImage = raw_flickr_images[index]
                photos.append(flickrImage)
            print((photos[0]))
            wikiText,raw_wiki_images = get_result("wikipedia", searchText)
            if len(raw_wiki_images) > 0:
                wikiImage = raw_wiki_images[0]
            twitterText,raw_twitter_images = get_result("twitter", searchText)
            return render_template('results.html', flickrImageList = photos, wikiText=wikiText,
                               wikiImage=wikiImage, searchText=searchText, twitterText=twitterText, username=username, searchTerm=searchTerm)
        email=session['email']
        username=session['username']
        searchList=dbHandler.showSearches(email)    
        return render_template('userHome.html', searchList=searchList)
    else:
        return render_template('index.html', message=None)
@app.route('/save', methods=['POST'])
def saveSearch():
    searchText = request.form['searchText']
    date = datetime.datetime.now()
    email=session['email']
    username = session['username']
    dbHandler.createSearch(email, searchText, date)
    return redirect(url_for('results'))
@app.route('/delete')
def deleteSearches():
    username = session['username']
    dbHandler.deleteSearches(username)
    return redirect(url_for('results'))

if __name__ == '__main__':
	app.secret_key = os.urandom(12)
	app.run(debug=True)
