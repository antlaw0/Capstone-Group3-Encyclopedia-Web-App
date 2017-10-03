#SQLite for project

import sqlite3
# maybe put into a function to text IF EXISTS, or initialize if doesn't?
conn = sqlite3.connect('banana.db')# connect to db
print ("Opened database successfully")

# create a table with 2 columns, search term is PKey
conn.execute("CREATE TABLE WIKIPEDIA"
         '(SEARCH_TERM TEXT PRIMARY KEY     NOT NULL,'
         'URL          TEXT    NOT NULL)')
print ("WIKI Table created successfully")

# create a table with 2 columns, search term is PKey
conn.execute("CREATE TABLE FLICKER"
         '(SEARCH_TERM TEXT PRIMARY KEY     NOT NULL,'
         'URL          TEXT    NOT NULL)')
print ("FLICKER Table created successfully")

# create a table with 2 columns, search term is PKey
conn.execute("CREATE TABLE TWITTER"
         '(SEARCH_TERM TEXT PRIMARY KEY     NOT NULL,'
         'URL          TEXT    NOT NULL)')
print ("TWITTER Table created successfully")

conn.commit() #commit the update
conn.close()#close the call

#  maybe put into a function once the correct table is id'd and initialized?
#variable to get the user searchterm, and the response URL?

# conn = sqlite3.connect('test.db')
# print ("Opened database successfully")
#
# conn.execute("INSERT INTO #XXXXXXXtablename# (ID,URL) \
#       VALUES (ID_variable, URL_variable )")

# conn.commit()#commit the update
# print ("Records created successfully")
# conn.close()#close the call