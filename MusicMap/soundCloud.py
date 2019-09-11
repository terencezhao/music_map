# -*- coding: utf-8 -*-
import soundcloud
import random
import urllib
import unicodedata
import pycountry
import countryinfo
from bs4 import BeautifulSoup

client = soundcloud.Client(client_id='cf588c295cb4b26a1fbe803f077833e2')
'''
    getTrackFromCountryCode returns a track url given a code
'''
def getTrackFromCountryCode(code):
    usernames = getUsernamesFromCountryCode(code)
    country = countryCodeToName(code)
    if not country:
        return
    return getCountryTrackFromUsernames(usernames,country, code)

'''
    getTrackFromCountryName returns a track url given a country name
'''
def getTrackFromCountryName(country):
    code = countryNameToCode(country)
    if not code:
        return
    usernames = getUsernamesFromCountryCode(code)
    track = getCountryTrackFromUsernames(usernames,country, code)
    return track

'''
    getTrackFromCityName returns a track url given a search for a city
    '''
def getTrackFromCityName(city):
    cityQueryURL ='http://soundcloud.com/people/search?q%5Bcountry_code%5D=&q%5Bcity%5D='
    urlSuffix = '&q%5Btype%5D%5Bartist%5D=on'
    modifiedQueryURL=cityQueryURL + city +urlSuffix
    searchPage = urllib.urlopen(modifiedQueryURL)
    soup = BeautifulSoup(searchPage)
    userElements = soup.find_all("div","user-name")
    users = []
    for userElement in userElements:
        try:
            username = userElement.get('title')
            users.append(username)
        except UnicodeEncodeError:
            break
    return getCityTrackFromUsernames(users,city)

'''
    getTrackFromStateName does a city query with the state name.
    Many users use the state name in place of a city if US
    '''
def getTrackFromStateName(state):
    return getTrackFromCityName(state);


'''
    getUsernamesFromCountryCode takes in a countrycode and returns a list of usernames
    This is parsed using beautiful sound and the soundcloud search URL
    '''
def getUsernamesFromCountryCode(code):
    countryQueryURL ='http://soundcloud.com/people/search?q%5Bcountry_code%5D='
    urlSuffix = '&q%5Btype%5D%5Bartist%5D=on'
    modifiedQueryURL=countryQueryURL + code +urlSuffix
    searchPage = urllib.urlopen(modifiedQueryURL)
    soup = BeautifulSoup(searchPage)
    userElements = soup.find_all("div","user-name")
    users = []
    for userElement in userElements:
        try:
            username = userElement.get('title')
            users.append(username)
        except UnicodeEncodeError:
            break
    return users

'''
    getCountryTrackFromUsernames takes in a country, code  and username list
    It then randomly chooses a user and randomly chooses a track from the first user in the list
    with tracks. The track url is returned
    
    '''
def getCountryTrackFromUsernames(usernames , country, code):
    tracks =[]
    random.shuffle(usernames)
    for username in usernames:
        try:
            users = client.get('/users', q=username)
            for user in users:
                userCode = altNameToCode(user.country)
                if((user.country and user.country.lower() == country.lower())
                   or (userCode and userCode == code)):
                    tracks.extend(client.get('/users/' + str(user.id) + '/tracks'))
                    if(len(tracks)>0):
                        random.shuffle(tracks)
                        return tracks[0].permalink_url
                    break
        except UnicodeEncodeError:
            break
    random.shuffle(tracks)
    if tracks:
        return tracks[0].permalink_url
    return


'''
    getCityTrackFromUsernames takes in a cityname and username list
    It then randomly chooses a user and randomly chooses a track from the first user in the list
    with tracks. The track url is returned
    
    '''
def getCityTrackFromUsernames(usernames , city):
    tracks =[]
    random.shuffle(usernames)
    for username in usernames:
        try:
            users = client.get('/users', q=username)
            for user in users:
                if(user.city and user.city.lower() == city.lower()):
                    tracks.extend(client.get('/users/' + str(user.id) + '/tracks'))
                    if(len(tracks)>0):
                        random.shuffle(tracks)
                        return tracks[0].permalink_url
        except UnicodeEncodeError:
            break
    random.shuffle(tracks)
    if tracks:
        return tracks[0].permalink_url
    return

def countryCodeToName(code):
    country = pycountry.countries.get(alpha2=code)
    if country:
        return country.name
    return


def countryNameToCode(CountryName):
    country = pycountry.countries.get(name=CountryName)
    if country:
        return country.alpha2
    return

def altNameToCode(countryName):
    countries = countryinfo.countries
    for country in countries:
        altName = country['name']
        
        if (altName and countryName and
            str(altName.lower()) == str(countryName.lower())):
            return country['code']
    return


