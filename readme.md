# Meeting Organizer

Meeting Organizer is a simple web app to organize meetings. It is developed in python by using Flask. It has 5 HTML tampletes for front-end. base.html is for base for html initialization and style issues.

index.html is for listing meetings. create.html is for creating new meeting. meeting.html is to see details of a specific meeting. edit.html is for updating meeting details.

## Environment Setup and Initialization:

To setup environment install required packages to virtual environment. Navigate to the project folder on cmd and install
requirements.

```bash
py -m venv env
.\env\Scripts\activate
pip install -r requirements.txt
```
To have a clear databese delete database.db from your folder and run inti_db.py

```bash
python init_db.py
```
Now, you get a database.db file in your folder. This is the database where information about meetings will be stored. 

Run meeting organizer.

```bash
python main.py
```

## How To Use Web Interface:

To reach web interface of meeting organizer type http://127.0.0.1:8080 to your browser.

Since the database is empty there is no meeting to list. To add first meeting click to Create Meeting button. Fill all
fields to create a new meeting and click the submit button. It is important that start time of the meeting is later than now.
Also end time of the meeting must be later than start time. When you submit a valid meeting you will be directed to index page
where you will see the list of the meetings.

Now, you can add a new meeting or see the details of meeting. When you click on the meeting details will be available on the page.
You can edit meeting information by clicking on edit meeting. After your edit finish you will be again directed to index page.
You can also delete the meeting by clicking delete meeting, or you can just go back to index page by clicking return meeting list.

## main.py:
Firstly import relevant libraries.
```python
from flask import Flask
from flask import request, render_template, request, url_for, flash, redirect
import sqlite3
from datetime import datetime
```
Configure app.
```python
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your key'
```
Method for database connection.
```python
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn
```
Method to get a meeting from database.
```python
def get_meeting(meeting_id):
    conn = get_db_connection()
    meeting = conn.execute('SELECT * FROM meetings WHERE id = ?',
                        (meeting_id,)).fetchone()
    conn.close()
    return meeting
```
index() method gets all meetings from databes and calls index.html to list all meetings.
```python
@app.route("/", methods=['GET', 'POST'])
def index():
    conn = get_db_connection()
    meetings = conn.execute('SELECT * FROM meetings').fetchall()
    conn.close()

    return render_template("index.html",meetings =meetings)
```
meeting() method gets a meeting from databes and calls meeting.html to show details of selected meeting.
```python
@app.route('/<int:meeting_id>')
def meeting(meeting_id):
    meeting = get_meeting(meeting_id)
    return render_template('meeting.html', meeting=meeting)
```
create() method presents create.html, gets user input from this form and inserts new meetings detaild to database.
Also, validity of inputs are checked here.
```python
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
```
edit() method gets meeting details from database and presents it to user to update them.
```python
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
```
delete() method removes sepecified meeting from database.
```python
@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    meeting = get_meeting(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM meetings WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" meeting was successfully deleted!'.format(meeting['topic']))
    return redirect(url_for('index'))
```
We run the app on local for development.
```python
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
```
