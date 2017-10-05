import sqlite3
from bottle import run, route, template,\
                   request, redirect, abort,\
                   static_file    

database = "Sqlite/pages.db"

@route('/static/<filepath:path>')
def static_files(filepath):
    return static_file(filepath, root="")

@route("/add", method="GET")
def write():
    return template("index.html", mess="")

@route('/add', method='POST')
def writed():
    global database
    con = sqlite3.connect(database)
    cur = con.cursor()
    data_form = request.forms.decode("utf-8")
    data_form_text = data_form["text"]
    title = data_form["title"]
    try:
        cur.execute('INSERT INTO entries (text, title) VALUES(?, ?)',
                    (data_form_text, title))
        con.commit()
    except sqlite3.OperationalError:
        cur.execute('''CREATE TABLE `entries` (
         Id	INTEGER PRIMARY KEY AUTOINCREMENT,
	 text	TEXT NOT NULL,
	 title	TEXT NOT NULL
        );''')
        cur.execute('INSERT INTO entries (text, title) VALUES(?, ?)',
                    (data_form_text, title))
        con.commit()
    return template("index.html", mess=\
                    "New entry was successfully posted")

@route('/blog/<id_blog>')
def display_entries(id_blog):
    global database
    con = sqlite3.connect(database)
    cur = con.cursor()
    mlist = []
    try:
        cur.execute('SELECT * FROM entries')
    except sqlite3.OperationalError:
        cur.execute('''CREATE TABLE `entries` (
         Id	INTEGER PRIMARY KEY AUTOINCREMENT,
	 text	TEXT NOT NULL,
	 title	TEXT NOT NULL
        );''')
        cur.execute('SELECT * FROM entries')
    for i in cur:
        mlist.append(i[0])
    try:
        if int(id_blog) in mlist:
            cur.execute('SELECT * FROM entries WHERE Id IN (%s);' % id_blog)
            for i in cur:
                #yield "<h1>%s</h1>" % i[2]
                #yield "<pre>%s\n</pre>" % i[1]
                return template("blog.html", title=i[2], text=i[1])
    except ValueError:
        abort(404, "Not found: '/blog/%s'" % str(id_blog))
    else:
        abort(404, "Not found: '/blog/%s'" % str(id_blog))
run(host="0.0.0.0", port="9000")
