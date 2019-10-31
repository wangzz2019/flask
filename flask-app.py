from flask import Flask,jsonify, render_template, request, Response, json, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


# Initialize DogStatsD and set the host.
#initialize(statsd_host = 'dd-agent')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:Password123!@jacktestdb.c3bw7kcbozbg.ap-northeast-1.rds.amazonaws.com/testdb'
db = SQLAlchemy(app)

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
    return render_template('show_all.html', peoples = test.query.all())

@app.route('/new', methods = ['GET', 'POST'])
def new():
    if request.method == 'POST':
       if not request.form['name']:
          flash('Please enter all the fields', 'error')
       else:
          people = test(request.form['name'], request.form['city'],request.form['addr'], request.form['pin'])
          print(people)
          db.session.add(people)
          db.session.commit()
          flash('Record was successfully added')
          return redirect(url_for('show_all'))
    return render_template('new.html')


if __name__ == "__main__":
  app.run()