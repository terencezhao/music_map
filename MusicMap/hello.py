#!/usr/bin/python

import soundCloud

from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/my-link/')
def my_link():
  print 'I got clicked!'
  return 'Click.'

@app.route('/country/<country>')
def getSongFromCountry(country):
    trackURL = soundCloud.getTrackFromCountryName(country)
    if country == "United States":
         return render_template('index.html', trackURL = trackURL, currentName = country, stateView="true")     
    return render_template('index.html', trackURL = trackURL, currentName = country, stateView="false")

@app.route('/state/<state>')
def getSongFromState(state):
	trackURL = soundCloud.getTrackFromStateName(state)
	return render_template('index.html', trackURL = trackURL, currentName = state, stateView="true")

@app.route('/city/<city>')
def getSongFromCity(city):
	trackURL = soundCloud.getTrackFromCityName(city)
	return render_template('index.html', trackURL=trackURL, currentName = city,
                           stateView = "false")

@app.route('/countrycode/<code>')
def getSongFromCountryCode(code):
    trackURL = soundCloud.getTrackFromCountryCode(code)
    print trackURL
    if code == "US":
        return render_template('index.html', trackURL = trackURL, currentName = code,
                               stateView = "true")
    return render_template('index.html', trackURL = trackURL, currentName = code,
                           stateView = "false")

if __name__ == '__main__':
  app.run()
