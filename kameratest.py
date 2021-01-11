import pyrebase
import time
from datetime import datetime
from decimal import Decimal
import json
from json import encoder
import Adafruit_DHT
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
from PIL import Image

#Firebase Init
config = {     
  "apiKey": "AIzaSyAeTF-VH5vxA0-ssHg4rMcjIodzBnnPvPw",
  "authDomain": "smartgrowsystem-sgs.firebaseapp.com",
  "databaseURL": "https://smartgrowsystem-sgs.firebaseio.com",
  "storageBucket": "smartgrowsystem-sgs.appspot.com"
}

firebase = pyrebase.initialize_app(config)  
db = firebase.database();

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.rotation = 180
rawCapture = PiRGBArray(camera)
fileName="photo"
path = "./images/";

#post to storage
def uploadImage(path,name):
	storage = firebase.storage();
	storage.child('/images/'+name).put(path+name);
	print("uploaded");

#write to database
def referenceImage(fileName,date):
	db.child("images").child(date).set(fileName);
	print("referenced");
	
def takePhoto():
	ts = datetime.now();
	date = ts.strftime("%Y-%m-%d %H:%M:%S");
	name = fileName+"_"+date+".jpg";
	
	# take Image and save it
	time.sleep(0.5)
	camera.capture(path+name)
	time.sleep(0.5)
	
	# uploadImage into firebase
	uploadImage(path,name);
	referenceImage(name,date);

def stream_handler(message):
	print(message);
	data = message["data"];
	print(data);
	if(data==True):
		takePhoto();
		db.child("photo").set(False);
		print("photo taken");

my_stream = db.child("photo").stream(stream_handler)

while True:
	
	takePhoto();
	print("photo taken");
	time.sleep(1);
