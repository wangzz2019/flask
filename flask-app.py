from flask import Flask

# Initialize DogStatsD and set the host.
#initialize(statsd_host = 'dd-agent')

app = Flask(__name__)

@app.route('/')
def hello():
    # Increment a Datadog counter.
    #statsd.increment('my_webapp.page.views')

    return "Hello World!"

if __name__ == "__main__":
  app.run()