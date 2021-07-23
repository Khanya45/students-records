import sqlite3
from flask import Flask, render_template, request, jsonify


def init_sqlite_db():
    connect = sqlite3.connect("database.db")
    print("open database successfully")

    connect.execute("CREATE TABLE IF NOT EXISTS tblstudents (name TEXT, address TEXT, city TEXT, pin TEXT)")
    print("Table created successfully")
    connect.close()


init_sqlite_db()

app = Flask(__name__)


@app.route('/enter-new/')
def enter_new_student():
    return render_template('student.htnl.html')


@app.route('/add-new-record/', methods=['POST'])
def add_new_student():
    msg = None
    if request.method == 'POST':
        try:
            name = request.form['name']
            address = request.form['address']
            city = request.form['city']
            pin = request.form['pin']

            with sqlite3.connect('database.db') as conn:
                cur = conn.cursor()
                cur.execute('INSERT INTO tblstudents (name, address, city, pin) VALUES(?,?,?,?)', (name, address, city, pin))
                conn.commit()
                msg = "Record successfully added"
        except Exception as e:
            conn.rollback()
            msg = "Error occured in insert:" + str(e)
        finally:
            # return render_template('result.html', msg=msg)
            with sqlite3.connect('database.db') as conn:
                cur = conn.cursor()
                cur.execute('SELECT * FROM tblstudents')
                results = cur.fetchall()
                # conn.close()
            return render_template('result.html', results=results)

