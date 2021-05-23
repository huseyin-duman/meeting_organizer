from flask import Flask
from flask import request, render_template, request, url_for, flash, redirect
import sqlite3
from datetime import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your key'

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_meeting(meeting_id):
    conn = get_db_connection()
    meeting = conn.execute('SELECT * FROM meetings WHERE id = ?',
                        (meeting_id,)).fetchone()
    conn.close()
    return meeting

@app.route("/", methods=['GET', 'POST'])
def index():
    conn = get_db_connection()
    meetings = conn.execute('SELECT * FROM meetings').fetchall()
    conn.close()

    return render_template("index.html",meetings =meetings)

@app.route('/<int:meeting_id>')
def meeting(meeting_id):
    meeting = get_meeting(meeting_id)
    return render_template('meeting.html', meeting=meeting)

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        topic = request.form['topic']
        date = request.form['date']
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        attendees = request.form['attendees']

        if not topic or not date or not start_time or not end_time or not attendees :
            flash("Please fill all fields")
        elif start_time>=end_time:
            flash("Meeting end time must be later than start time.")
        elif datetime.date(datetime.now())>datetime.strptime(date,"%Y-%m-%d").date():
            flash("Meeting date must not be earlier than today.")
        elif datetime.date(datetime.now()) == datetime.strptime(date, "%Y-%m-%d").date() and datetime.now().time()>datetime.strptime(start_time,"%H:%M").time():
            flash("Meeting start time must be later than now.")
        else:
            conn = get_db_connection()
            conn.execute("INSERT INTO meetings (topic, date, start_time, end_time, attendees) VALUES (?, ?,?, ?, ?)",
                         (topic, date, start_time, end_time, attendees))

            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    meeting = get_meeting(id)

    if request.method == 'POST':
        topic = request.form['topic']
        date = request.form['date']
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        attendees = request.form['attendees']

        if not topic or not date or not start_time or not end_time or not attendees :
            flash("Please fill all fields")
        elif start_time>=end_time:
            flash("Meeting end time must be later than start time.")
        elif datetime.date(datetime.now())>datetime.strptime(date,"%Y-%m-%d").date():
            flash("Meeting date must not be earlier than today.")
        elif datetime.date(datetime.now()) == datetime.strptime(date, "%Y-%m-%d").date() and datetime.now().time()>datetime.strptime(start_time,"%H:%M").time():
            flash("Meeting start time must be later than now.")
        else:
            conn = get_db_connection()
            conn.execute("UPDATE meetings SET topic = ?, date = ?, start_time = ?, end_time = ?, "
                         "attendees = ? WHERE id = ?  ",
                         (topic, date, start_time, end_time, attendees, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', meeting=meeting)

@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    meeting = get_meeting(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM meetings WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" meeting was successfully deleted!'.format(meeting['topic']))
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)