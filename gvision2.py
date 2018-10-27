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

api = "AIzaSyDTq4cci16u92_lonCb5CA2oBhYvWagc3I"
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
    required_entities = {'ORGANIZATION': '', 'PERSON': '', 'LOCATION': '', 'DATE': ''}
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
#    with open(filepath, 'r') as f:
#    	file = f.read()
    x = re.findall('\d\d.\d\d.\d\d\d\d', filepath)
    y = []
    for item in x:
        try:
            date = datetime.datetime.strptime(item, datepattern)
            date = date.date()
            age = dateutil.relativedelta.relativedelta(now,date)
            age = age.years
            y.append(age)    	
        except:
            pass
    for item in y:
        if item >15:
            return item
    return item

def getdate2(txt):
    filepath = txt
    datepattern = '%b %y'
#    with open(filepath, 'r') as f:
#    	file = f.read()
    x = re.findall('\S\S\S \d\d', filepath)
    y = []
    for item in x:
        try:
            date = datetime.datetime.strptime(item, datepattern)
            date = date.date()
            age = dateutil.relativedelta.relativedelta(now,date)
            age = age.years
            y.append(age)
        except:
            pass
    for item in y:
        if item > 15:
            return item
    return item

mytxt1 = detect_text("bpass1.jpg", api)
mytxt2 = detect_text("bpass2.jpg", api)
mytxt3 = detect_text("bpass3.jpg", api)
mytxt4 = detect_text("bpass4.jpg", api)
mytxt5 = detect_text("bpass5.jpg", api)
mytxt6 = detect_text("bpass6.jpg", api)
travel = pd.read_csv("city_abbreviation.csv", sep = ",", encoding = "ISO-8859-1")
travel2 = travel[:,1]
travel3 = list(travel2)
#spl1 = mytxt1.replace("\n", ".")
from geotext import GeoText
