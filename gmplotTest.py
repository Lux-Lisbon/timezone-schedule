from gmplot import gmplot
import webbrowser
# import os
# from urllib.request import pathname2url # Python 3.x
import flask

# Initialize the map at a given point
apikey = "AIzaSyDsJB_s4ZeOasA6CDQ67bvb6iw48YPcVyk"

def gMapPlot(lat,long):
    gmap = gmplot.GoogleMapPlotter(lat,long,14,apikey=apikey)
    # Add a point
    gmap.marker(lat,long,'cornflowerblue')
    # Draw google map into HTML file
    gmap.draw("templates/my_map.html")

    app = flask.Flask(__name__)

    @app.route('/')
    def index():
      return flask.render_template('my_map.html')

    app.run('0.0.0.0',8080)
