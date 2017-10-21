"""
This is used to hold database functions
"""

import sqlite3 as sql

def insertUser(email, username,password):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO users (email, username, password) VALUES (?,?, ?)", (email, username,password))
    con.commit()
    con.close()

	
def retrieveUsers():
	con = sql.connect("database.db")
	cur = con.cursor()
	cur.execute("SELECT username, password FROM users")
	users = cur.fetchall()
	con.close()
	return users


	
#This method takes a string and returns whether or not a user with the email enter exists
def userExists(email):
	email=email
	con = sql.connect("database.db")
	c = con.cursor()
	c.execute("SELECT email FROM users WHERE email = ?", (email,))
	#format(tn='users'))
	data=c.fetchall()
	if len(data)==0:
		print("User with e-mial "+email+" not found")
		return False
	else:
		print("User with e-mail "+email+" found")
		return True
	con.close()
	
#gets users searches, returns list of searches
def showSearches(email):
	
	conn = sql.connect('database.db')
	c = conn.cursor()
	
	c.execute("SELECT KeyWord, TimeStamp FROM UserSaves INNER JOIN users ON UserSaves.id_column = users.id_column WHERE email=?",(email,))
	searchList=list(c.fetchall())
	print(searchList)
	return searchList

	
def deleteUser(email):
	
	con = sql.connect("database.db")
	c = con.cursor()
	if userExists(email)==True:
		c.execute("DELETE FROM users WHERE username=?", (email,))
		print("User with email "+email+" has been deleted.")
	else:
		print("User does not exist.")
	con.commit()
	con.close()

	
def getPassword(email):
	email=email
	con = sql.connect("database.db")
	c = con.cursor()
	c.execute("SELECT password FROM users WHERE email = ?", (email,))
	#format(tn='users'))
	data=c.fetchall()
	d=data[0]
	#print(data[0])
	return d[0]
	con.close()

def getUsername(email):
	email=email
	con = sql.connect("database.db")
	c = con.cursor()
	c.execute("SELECT username FROM users WHERE email = ?", (email,))
	#format(tn='users'))
	data=c.fetchall()
	d=data[0]
	#print(data[0])
	return d[0]
	con.close()

	
#returns the ID of a given email
def getId(email):
	
	con = sql.connect("database.db")
	c = con.cursor()
	c.execute("SELECT id_column FROM users WHERE email = ?", (email,))
	data=c.fetchall()
	d=data[0]
	#print("ID: "+str(d[0]))
	return d[0]
	con.close()

#inserts a search
def createSearch(email, searchTerm, time):
	
	uid=getId(email)
	searchTerm=searchTerm
	time=time
	conn = sql.connect('database.db')
	c = conn.cursor()

	c.execute("INSERT INTO UserSaves (id_column, Keyword, TimeStamp) VALUES (?, ?, ?)",(uid, searchTerm, time,))
	conn.commit()
	conn.close()
def deleteSearches(email):
	conn = sql.connect('database.db')
	c = conn.cursor()
	uid = getId(email)
	c.execute("DELETE FROM UserSaves WHERE id_column = ?", (uid,))
	conn.commit()
	conn.close()

	