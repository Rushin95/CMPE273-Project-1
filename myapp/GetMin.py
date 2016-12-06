from flask import render_template, redirect, request, flash, url_for, json, make_response
from flask_mail import Message
from flask_googlemaps import Map, icons
from google_api import *
from forms import *
from myapp import app, mail, db
from decimal import Decimal

def UberMin(uberdata):
    #UberModify=uberdata
    if 'OptimizedRoute' in uberdata: del uberdata['OptimizedRoute']
    test=uberdata
    dict={}
    length=len(test)
    print "IN Get Min Function"
    #print length
    for key in test.iteritems():
             dict[key[0]]=key[1]['Price']

    print dict
    minvalue=min(dict, key=dict.get)
    return minvalue

def Lyftmin(lyftdata):
    dict={}
    for key in lyftdata.iteritems():
        if(key[1]['avg_cost'] > 0):
            dict[key[0]]=key[1]['avg_cost']
    minvalue=min(dict, key=dict.get)
    print minvalue
    return minvalue
