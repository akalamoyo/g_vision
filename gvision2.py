# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 15:19:46 2017

@author: moyo.akala
"""

# -*- coding: utf-8 -*-
import base64
import requests
import re
import datetime
import dateutil
import pandas as pd
from geotext import GeoText
api = "INPUT API KEY HERE"

def detect_text(image_file, access_token=None):

    with open(image_file, 'rb') as image:
        base64_image = base64.b64encode(image.read()).decode()

    url = 'https://vision.googleapis.com/v1/images:annotate?key={}'.format(access_token)
    header = {'Content-Type': 'application/json'}
    body = {
        'requests': [{
            'image': {
                'content': base64_image,
            },
            'features': [{
                'type': 'TEXT_DETECTION',
                'maxResults': 1,
            }]

        }]
    }
    response = requests.post(url, headers=header, json=body).json()
    text = response['responses'][0]['textAnnotations'][0]['description'] if len(response['responses'][0]) > 0 else ''
    return text

def extract_entities(text, access_token=None):

    url = 'https://language.googleapis.com/v1beta1/documents:analyzeEntities?key={}'.format(access_token)
    header = {'Content-Type': 'application/json'}
    body = {
        "document": {
            "type": "PLAIN_TEXT",
            "language": "EN",
            "content": text
        },
        "encodingType": "UTF8"
    }
    response = requests.post(url, headers=header, json=body).json()
    return response


def extract_required_entities(text, access_token=None):
    entities = extract_entities(text, access_token)
    required_entities = {'LOCATION': ''}
    for entity in entities['entities']:
        t = entity['type']
        if t in required_entities:
            required_entities[t] += entity['name']

    return required_entities

def getdate(txt):
    now = datetime.datetime.utcnow()
    now = now.date()
    filepath = txt
    datepattern = '%d.%m.%Y'
    datepattern2 = '%b %y'
#    with open(filepath, 'r') as f:
#    	file = f.read()
    x = re.findall('\d\d.\d\d.\d\d\d\d', filepath)
    x2 = re.findall('\S\S\S \d\d', filepath)
    if not x:
        x = x2
        datepattern = datepattern2
    y = []
    for item in x:
        try:
            date = datetime.datetime.strptime(item, datepattern)
            date = date.date()
            age = dateutil.relativedelta.relativedelta(now,date)
            age = age.years
            y.append(age)    	
        except ValueError:
            pass
    for item in y:
        if item >15:
            return item
    return item
      
mytxt1 = detect_text(/pics/british.png',api)
#mytxt1 = detect_text('/pics/british.png',api)
#mytxt1
#mytxt2 = detect_text('/pics/Intl.jpg',api)
mytxt3 = detect_text('/pics/driver.jpg',api)
mytxt4 = detect_text('/pics/bpass1.jpg',api)
mytxt5 = detect_text('/pics/bpass3.jpg',api)
mytxt6 = detect_text('/pics/bpass6.jpg',api)
mytxt7 = detect_text('/pics/bpass5.jpg',api)
mytxt8 = detect_text('/pics/bpass2.jpg',api)

#
#
#spl5 = mytxt5.replace(" ", ".")
#spl6 = mytxt6.replace(" ", ".")
#spl7 = mytxt7.replace(" ", " ")
#places5 = GeoText(spl5)
#places6 = GeoText(spl6)
#places7 = GeoText(spl7)
#places7.cities


cities = pd.read_csv("cities.txt", sep = "\t", encoding = 'ISO-8859-1')
cities = cities[['Cities','Countries','Abbr']]
cities_names = cities.iloc[:,0]
cities_abbr = cities.iloc[:,2]
cities_names = list(cities_names)
cities_abbr = list(cities_abbr)

def extract_location(text):
    i = 0
    location = []
    mytxt = text
    mytxt = mytxt.splitlines()
    list2 = set(mytxt)&set(cities_abbr)
    list3 = set(mytxt)&set(cities_names)
    list4 = sorted(list3, key = lambda k : mytxt.index(k))
    if not list4:
        list4 = sorted(list2, key = lambda k: mytxt.index(k))
        for i in [0,1]:
            loca = (cities[cities['Abbr'] == list4[i]])
            location.append(loca)
    return location

def extract_location2(text):
    i = 0
    location = []
    text = text.replace(" ", "\n")
    text = text.replace(" → ", "\n")
    mylist = text.splitlines()
    list2 = set(mylist)&set(cities_abbr)
    list4 = sorted(list2, key = lambda k: mylist.index(k))
    for i in [0,1]:
        loca = (cities[cities['Abbr'] == list4[i]])
        location.append(loca)
    return location

extract_location2(mytxt3)
getdate(mytxt3)
