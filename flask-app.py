from flask import Flask,jsonify, render_template, request, Response, json, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask.helpers import flash
import os
import pymysql
pymysql.install_as_MySQLdb()
from google.cloud import spanner, firestore_v1
# from google.cloud import firestore
from ddtrace import tracer,config



#GCP Cloud Spanner
# Imports the Google Cloud Client Library.
#from google.cloud import spanner

# Initialize DogStatsD and set the host.
#initialize(statsd_host = 'dd-agent')

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = os.urandom(24)

#AWS RDS
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://xxx:xxx@jacktestdb.c3bw7kcbozbg.ap-northeast-1.rds.amazonaws.com/testdb'
db = SQLAlchemy(app)

class test(db.Model):
    id = db.Column('id', db.Integer, primary_key = True)
    name = db.Column(db.String(50))
    def __init__(self, name):
        self.name = name

class people():
    def __init__(self,id,name):
        self.id=id
        self.name = name

@app.route("/firestore",methods=['GET','POST'])
#@tracer.wrap()
def firestore():
    config.grpc["service"]="Google Firestore"
    #GCP firestore
    # firestore_client = firestore.Client(project='datadog-sandbox')
    firestore_client=firestore_v1.Client()
    doc_ref = firestore_client.collection(u'users').document(u'namelist1')
    doc_ref.set({
        u'first': u'Jack',
        u'last': u'Wang',   
        u'born': 1982
    })
    doc_ref = firestore_client.collection(u'users').document(u'namelist2')
    doc_ref.set({
        u'first': u'Zhizheng',
        u'middle': u'Jack',
        u'last': u'Wang',
        u'born': 1982
    })
    users_ref = firestore_client.collection(u'users')
    docs = users_ref.stream()
    peoples=[]
    for doc in docs:
        i=1
        print(f'{doc.id} => {doc.to_dict()}')
        peoples.append(people(i,doc.to_dict()['first']))
        i=i+1

    return render_template('show_all.html',peoples = peoples)
  

@app.route("/gsp",methods=['GET','POST'])
#@tracer.wrap()
def gsp():
    #GCP Cloud Spanner
    # Instantiate a client.
    config.grpc["service"]="Google Spanner"
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
    #pan = tracer.trace('spanner.sql')
    with database.snapshot() as snapshot:
        results = snapshot.execute_sql('SELECT * from testtb')
        peoples=[]
        for result in results:
            peoples.append(people(result[0],result[1]))
        # for people in results:
        #     peoples.list.addpend(people.name)
        #span.finish()
        return render_template('show_all.html',peoples = peoples)



@app.route('/')
def show_all():
    #Increment a Datadog counter.
    #statsd.increment('my_webapp.page.views')
    db=SQLAlchemy(app)
    return render_template('show_all.html', peoples = test.query.all())
    
@app.route('/test')
def testpage():
    return "this is a test response created by Mike"

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
  port = int(os.getenv("PORT", 8081))
  app.run(host="0.0.0.0",port=port)
