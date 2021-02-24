from datetime import datetime
import firebase

temperatures = {} 
humidites = {}

def readData(newTemp,newHum):
    global temperatures
    global humidites
    
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    temperatures[current_time] = newTemp
    humidites[current_time] = newHum

    firebase.writeLiveData("temperature",newTemp)
    firebase.writeLiveData("humidity",newHum)

    firebase.writeChild("temperatures",temperatures[current_time])



    print(temperatures)
    print(humidites)

    

