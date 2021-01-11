import pyrebase
import time
from datetime import datetime
import simpletest

config = {     
  "apiKey": "AIzaSyAeTF-VH5vxA0-ssHg4rMcjIodzBnnPvPw",
  "authDomain": "smartgrowsystem-sgs.firebaseapp.com",
  "databaseURL": "https://smartgrowsystem-sgs.firebaseio.com/",
  "storageBucket": "smartgrowsystem-sgs.appspot.com"
}

firebase = pyrebase.initialize_app(config)  
db = firebase.database()
pin = '4'

print(simpletest.humidity)


#while(True):
    #ts = datetime.now()
   # db.child("temperature").set(actualtemp)
    #db.child("temperatures").child(ts.strftime("%d:%m:%Y, %H:%M:%S")).set(actualtemp)
   # time.sleep(3)