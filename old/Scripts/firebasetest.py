import pyrebase
import time
from datetime import datetime
import sensors


config = {
    "apiKey": "AIzaSyAeTF-VH5vxA0-ssHg4rMcjIodzBnnPvPw",
    "authDomain": "smartgrowsystem-sgs.firebaseapp.com",
    "databaseURL": "https://smartgrowsystem-sgs.firebaseio.com/",
    "storageBucket": "smartgrowsystem-sgs.appspot.com"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

user = auth.sign_in_anonymous()
token = user['idToken']

db = firebase.database()


pin = '4'


def getChildValue(name):
    print(token)
    value = db.child("activeClimate").get(token=token).val()
    print(value)
    return value


def saveValues():
    # get timestamp
    ts = datetime.datetime.now()

    # get sensor data
    humidity, temperature = readValue()

    # format data
    formathumidity = '%.2f' % humidity
    formattemperature = '%.2f' % temperature

    print(formattemperature)
    print(formathumidity)
    # set sensor data in firebase
    # temperature
    db.child("temperature").set(formattemperature)
    db.child("temperatures").child(ts.strftime(
        "%Y-%m-%d %H:%M:%S")).set(formattemperature)
    # humidity
    db.child("humidity").set(formathumidity)
    db.child("humiditys").child(ts.strftime(
        "%Y-%m-%d %H:%M:%S")).set(formathumidity)


activeClimate = getChildValue("activeClimate")

print(activeClimate)
