# Main Function of the SUF Script
# use command to start: python3 main.py >> output.txt
from modules.objects.climate import Climate
from modules.lamp import sunTimeChanged
import multiprocessing
import time
from multiprocessing import Process, shared_memory, Value, Lock
from datetime import datetime

import modules.database as db
import modules.sensors as sensors
import modules.watering as ir
import modules.lamp as light
from modules.loop import loop


def getCurrentTimeString():
    now = datetime.now()
    return now.strftime("%d.%m.%Y %H:%M:%S")


def readSensors(temperature, humidity, soilMoisture, lock):

    sensors_process = Process(
        target=sensors.readValues, args=(temperature, humidity, soilMoisture, lock))
    sensors_process.start()
    print(f"Sensors Process has started @{getCurrentTimeString()}")
    sensors_process.join()
    print(f"Sensors Process has finished @{getCurrentTimeString()}")
    return temperature.value, humidity.value, soilMoisture.value,


def main():
    # Init Variables
    samplingTime = 60
    irrigated = False
    irrigationTime = datetime.today().replace(hour=12, minute=0)
    activeClimate = Climate('', empty=True)
    temperature = Value('d', 0)
    humidity = Value('d', 0)
    soilMoisture = Value('d', 0)
    waterTankLevel = Value('d', 0)
    growProgress = Value('d', 0)
    amount = Value("d", 0)
    percentage = Value("d", 0)

    print(f"SUF-Box Script has started @{getCurrentTimeString()}")

    # Firebase Stream Handler
    firebase_process = Process(
        target=db.firebaseMain, args=())
    firebase_process.start()
    print(f"Firebase Process has started @{getCurrentTimeString()}")

    # Main Loop which will control all regulations
    loopGen = loop(samplingTime)
    liveDataLock = Lock()

    while(True):
        print(f"Loop has repeated @{getCurrentTimeString()}")
        # Active Climate
        activeClimate = loadClimate()
        print(activeClimate.growPhase)

        # Irrigation
        if(irrigationTime.day != datetime.now().day):
            irrigationTime = irrigationTime.replace(day=datetime.now().day)
            irrigated = False
        if(irrigationTime.hour == datetime.now().hour and irrigated == False):
            irrigation()
            irrigated = True

        # Lamp

        lamp(activeClimate.getSuntime(activeClimate.growPhase.phase))

        # Sensors
        oldTemp = temperature.value
        oldHum = humidity.value
        oldSoil = soilMoisture.value
        readSensors(temperature, humidity, soilMoisture, liveDataLock)

        # LiveData
        updateLiveData(temperature, humidity, soilMoisture,
                       growProgress, waterTankLevel, liveDataLock)

        loopGen.__next__()
        print(getCurrentTimeString())


def shutdown():
    print(shutdown)


def lamp(suntime):
    lamp_Process = Process(
        target=light.sunTimeChanged, args=(suntime, suntime))
    lamp_Process.start()
    lamp_Process.join()


def irrigation(amount, percentage):
    irrigation_Process = Process(
        target=ir.irrigationStart, args=(amount, percentage))
    irrigation_Process.start()
    irrigation_Process.join()

    print()


def updateLiveData(temperature, humidity, soilMoisture, growProgress, waterTankLevel, liveDataLock):
    liveDataProcess = Process(
        target=db.updateLiveData, args=(temperature, humidity, soilMoisture, growProgress, waterTankLevel, liveDataLock))
    liveDataProcess.start()
    liveDataProcess.join()


def loadClimate():
    existing_shm = shared_memory.SharedMemory(
        name='activeClimate')

    buffer = existing_shm.buf
    json = buffer[:].tobytes().decode()
    climate = db.Climate(json)

    print(f"Active Climate has been loaded @{getCurrentTimeString()}")
    return climate


def firebase_main(main):
    ''' This function sends the data for the child process '''
    main.send(['Hello'])
    main.close()


def accurate_delay(delay):
    ''' Function to provide accurate time delay in millisecond
    '''
    _ = time.perf_counter() + delay/1000
    while time.perf_counter() < _:
        pass


if __name__ == "__main__":
    main()
