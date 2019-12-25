from flask import Flask,jsonify, render_template, request, Response, json, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask.helpers import flash
import os
from google.cloud import spanner

#GCP Cloud Spanner
# Imports the Google Cloud Client Library.
#from google.cloud import spanner

# Initialize DogStatsD and set the host.
#initialize(statsd_host = 'dd-agent')

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = os.urandom(24)

#AWS RDS
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:Password123!@jacktestdb.c3bw7kcbozbg.ap-northeast-1.rds.amazonaws.com/testdb'
db = SQLAlchemy(app)

#GCP Cloud Spanner
# Instantiate a client.
spanner_client = spanner.Client(project='datadog-sandbox')

# Your Cloud Spanner instance ID.
instance_id = 'jacktest'

# Get a Cloud Spanner instance by ID.
instance = spanner_client.instance(instance_id)

# Your Cloud Spanner database ID.
database_id = 'testdb'

# Get a Cloud Spanner database by ID.
database = instance.database(database_id)

# Execute a simple SQL statement.
with database.snapshot() as snapshot:
    results = snapshot.execute_sql('SELECT * from testtb')

    for row in results:
        print(row)



class test(db.Model):
    id = db.Column('id', db.Integer, primary_key = True)
    name = db.Column(db.String(50))
    def __init__(self, name):
        self.name = name

@app.route('/')
def show_all():
    # Increment a Datadog counter.
    #statsd.increment('my_webapp.page.views')
    #db=SQLAlchemy(app)
    #return render_template('show_all.html', peoples = test.query.all())
    with database.snapshot() as snapshot:
        results = snapshot.execute_sql('SELECT * from testtb')
        peoples=results
        for people in peoples:
            print(people)
    return render_template('show_all.html', peoples = results)

@app.route('/new', methods = ['GET', 'POST'])
def new():
    if request.method == 'POST':
       if not request.form['name']:
          flash('Please enter all the fields', 'error')
       else:
          #people = test(request.form['name'], request.form['city'],request.form['addr'], request.form['pin'])
          people=test(request.form['name'])
          print(people)
          db.session.add(people)
          db.session.commit()
          flash('Record was successfully added')
          return redirect(url_for('show_all'))
    return render_template('new.html')


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5123)