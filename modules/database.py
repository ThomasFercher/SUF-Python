from firebase import Firebase
import json
from ctypes import Structure, c_double


config = {
    "apiKey": "AIzaSyAeTF-VH5vxA0-ssHg4rMcjIodzBnnPvPw",
    "authDomain": "smartgrowsystem-sgs.firebaseapp.com",
    "databaseURL": "https://smartgrowsystem-sgs.firebaseio.com/",
    "storageBucket": "smartgrowsystem-sgs.appspot.com"

}

firebase = Firebase(config)
db = firebase.database()
auth = firebase.auth()
token = "asd"


def init():
    authApp()
    getClimateSettings()


def getClimateSettings():
    global token
    json_payload = db.child("activeClimate").get(token=token).val()
    json_data = json.dumps(json_payload, indent=4, default=str)
    climate = Climate(json_data)
    print(climate.GrowPhase.phase)

    print("Successfully loaded Climate Settings")


def authApp():
    global token
    user = auth.sign_in_with_email_and_password(
        email="suf.raspberry.python@gmail.com", password="sufpython")
    token = user["idToken"]
    print("Successfully authenticated App")


class Climate(Structure):
    _fields_ = [('x', c_double), ('y', c_double)]

    def __init__(self, data):
        self.__dict__ = json.loads(data)
        self.automaticWatering = self.__dict__["automaticWatering"]
        self.id = self.__dict__["id"]
        self.name = self.__dict__["name"]
        self.soilMoisture = self.__dict__["soilMoisture"]
        self.waterConsumption = self.__dict__["waterConsumption"]
        self.GrowPhase = GrowPhase(self.__dict__["growPhase"])


class GrowPhase(object):

    def __init__(self, data):

        self.phase = data["phase"]
        self.flower_hum = data["flower_hum"]
        self.flower_suntime = data["flower_suntime"]
        self.flower_temp = data["flower_temp"]
        self.lateflower_hum = data["lateflower_hum"]
        self.lateflower_suntime = data["lateflower_suntime"]
        self.lateflower_temp = data["lateflower_temp"]
        self.vegetation_hum = data["vegation_hum"]
        self.vegetation_suntime = data["vegation_suntime"]
        self.vegetation_temp = data["vegation_temp"]
