"""
This is used to hold database functions
"""

import sqlite3 as sql

def insertUser(username,password):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO users (username,password) VALUES (?,?)", (username,password))
    con.commit()
    con.close()

def retrieveUsers():
	con = sql.connect("database.db")
	cur = con.cursor()
	cur.execute("SELECT username, password FROM users")
	users = cur.fetchall()
	con.close()
	return users

#This method takes a string and returns whether or not a user with the username enter exists
def userExists(uname):
	uname=uname
	con = sql.connect("database.db")
	c = con.cursor()
	c.execute("SELECT username FROM users WHERE username = ?", (uname,))
	#format(tn='users'))
	data=c.fetchall()
	if len(data)==0:
		print(uname+" not found")
		return False
	else:
		print(uname+" found")
		return True
	con.close()
	
#gets users searches
def showSearches(uname):
	uname=uname
	conn = sql.connect('database.db')
	c = conn.cursor()
	username = uname
	c.execute("SELECT KeyWord, TimeStamp FROM UserSaves INNER JOIN users ON UserSaves.id_column = users.id_column WHERE username=?",(username,))
	print(c.fetchall())

	
def deleteUser(uname):
	uname=uname
	con = sql.connect("database.db")
	c = con.cursor()
	if userExists(uname)==True:
		c.execute("DELETE FROM users WHERE username=?", (uname,))
		print("User: "+uname+" has been deleted.")
	else:
		print("User does not exist.")
	con.commit()
	con.close()

	
def getPassword(uname):
	uname=uname
	con = sql.connect("database.db")
	c = con.cursor()
	c.execute("SELECT password FROM users WHERE username = ?", (uname,))
	#format(tn='users'))
	data=c.fetchall()
	d=data[0]
	#print(data[0])
	return d[0]
	con.close()
	
	