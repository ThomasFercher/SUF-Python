import modules.watering as ir
import modules.temperatureRegulation as tr
#import modules.adc as adc
import modules.sensors as sensors
import modules.camera as c
import modules.humidityRegulation as humr
import modules.watering as wat
import modules.lamp as lamp
import modules.servo as servo
from multiprocessing import Process, shared_memory, Value, Lock
from time import sleep


air = 20208
water = 9760

range = (air-water) / 100


def main():

    

    #tempTest()
    #irrigationTest()
    #humTest()
    #sensors
    

    dht22Test()
    soilMoistureTest()

    #camera
    c.takePhoto()

    testServo()
    
    #humidity Regulation
    #toggleAbluft()
    #humr.squirt(1)

    #servo
    #servo.openValve()
    #time.sleep(10)
    #servo.closeValve()


    #Irrigation
    #irrigationTest()



    


def irrigationTest():
    irtest = Process(
        target=ir.irrigationStart, args=(5.0, None))
    irtest.start()
    irtest.join()

def tempTest():
    trtest = Process(
        target=tr.temperatureRegulationCycle, args=(20, 18, 25))
    trtest.start()
    trtest.join()


def humTest():
    humt = Process(
        target=humr.squirt, args=(15.0,None))
    humt.start()
    humt.join()

def toggleAbluft():
    humr.changeAir()

def testServo():
    servotest = Process(
        target=servo.testServo, args=())
    servotest.start()
    servotest.join()




def dht22Test():
    temp,hum = sensors.readDHT()
    print(temp,hum)
    

def soilMoistureTest():
    val = sensors.readSoilMoisture()
    print(val)

def a():

    camera.takePhoto()


main()
