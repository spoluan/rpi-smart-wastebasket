# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 21:47:25 2022

@author: TRIJAYA
"""

import pyrebase

def senddata(persentage, paper, bottle, aluminium_can, foil_pack):

    config = {

        "apiKey": "AIzaSyAt0sB7nYpbLWtXMd-4ttEz6JcELf1-2Xc",
        "authDomain": "tseg-ac7df.firebaseapp.com",
        "projectId": "tseg-ac7df",
        "storageBucket": "tseg-ac7df.appspot.com",
        "messagingSenderId": "844272740394",
        "appId": "1:844272740394:web:222ae9d63acfb2de817b53",
        "measurementId": "G-7YSX0FF37X",
        "databaseURL": "https://tseg-ac7df-default-rtdb.firebaseio.com"

    }
    firebase = pyrebase.initialize_app(config)

    db = firebase.database()
    battery_data = {
        "percentage": persentage,
        "current": 1,
        "voltage": 3,
        "capacity": 500
    }

    capacity_data = {
        "paper": paper,
        "bottle": bottle,
        "aluminium_can": aluminium_can,
        "foil_pack": foil_pack
    }

    # write data to db: recent and history value
    db.child("tseg").child("battery").push(battery_data)
    db.child("tseg").child("capacity").push(capacity_data)
    db.child("tseg").child("battery_last").set(battery_data)
    db.child("tseg").child("capacity_last").set(capacity_data)

    # get data from db
    get_bat_data = db.child("tseg").child("battery").get()
    get_cap_data = db.child("tseg").child("capacity").get()
    get_recent_bat_data = db.child("tseg").child("battery_last").get()
    get_recent_cap_data = db.child("tseg").child("capacity_last").get()

    ''' print(get_bat_data.val())
    print(get_recent_bat_data.val())
    print(get_cap_data.val())
    print(get_recent_cap_data.val()) '''
