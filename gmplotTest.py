from gmplot import gmplot
# import os
# from urllib.request import pathname2url # Python 3.x
import flask
from flask import request

# Initialize the map at a given point
apikey = "AIzaSyDsJB_s4ZeOasA6CDQ67bvb6iw48YPcVyk"
app = flask.Flask(__name__)

def gMapPlot(lat,long):
    gmap = gmplot.GoogleMapPlotter(lat,long,14,apikey=apikey)
    # Add a point
    gmap.marker(lat,long,'cornflowerblue')
    # Draw google map into HTML file
    gmap.draw("templates/my_map.html")

    @app.route('/')
    def index():
      return flask.render_template('my_map.html')

    app.run('0.0.0.0',8080)

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
  
@app.route('/shutdown', methods=['GET'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'


# from klein import run, route

# @route('/')
# def home(request):
#     return 'Hello, world!'

# run("localhost", 8080)