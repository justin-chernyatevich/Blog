import sqlite3
from bottle import run, route, template, \
    request, abort, \
    static_file

database = "Sqlite/pages.db"
con = sqlite3.connect(database)
cur = con.cursor()


def init_db():
    try:
        cur.execute('''CREATE TABLE `entries` (
                     Id	INTEGER PRIMARY KEY AUTOINCREMENT,
    	            text	TEXT NOT NULL,
    	            title	TEXT NOT NULL
                        );''')
    except sqlite3.OperationalError:
        pass


@route("/static/<file_path>")
def static_files(file_path):
    return static_file(file_path, root="static/")


@route("/add", method="GET")
def write():
    return template("add_blog.html", mess="")


@route('/add', method='POST')
def edited():
    global database
    con = sqlite3.connect(database)
    cur = con.cursor()
    data_form = request.forms.decode("utf-8")
    data_form_text = data_form["text"]
    title = data_form["title"]
    if data_form_text != "" and title != "":
        cur.execute('INSERT INTO entries (text, title) VALUES(?, ?)',
                        (data_form_text, title))
        con.commit()
        return template("add_blog.html", mess="New entry was successfully posted")
    else:
        return template("add_blog.html", mess="Write error")


@route('/')
def dis_blog():
    cur.execute('SELECT * FROM entries')
    rows = cur.fetchall()
    return template("index.html", mess=rows)


@route('/blog/<id_blog>')
def display_entries(id_blog):
    my_list = []
    cur.execute('SELECT * FROM entries')
    for i in cur:
        my_list.append(i[0])
    try:
        if int(id_blog) in my_list:
            cur.execute('SELECT * FROM entries WHERE Id IN (%s);' % id_blog)
            for i in cur:
                # yield "<h1>%s</h1>" % i[2]
                # yield "<pre>%s\n</pre>" % i[1]
                return template("blog.html", title=i[2], text=i[1])
    except ValueError:
        abort(404, "Not found: '/blog/%s'" % str(id_blog))
    else:
        abort(404, "Not found: '/blog/%s'" % str(id_blog))


init_db()
run(host="0.0.0.0", port="9100")
