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
import modules.temperatureRegulation as tr
import modules.humidityRegulation as hum
from modules.loop import loop


def main():
    # Init Db
    token = db.authApp()
    firebase_process = Process(
        target=db.firebaseMain, args=(token, ""))
    firebase_process.start()
    print(f"Firebase Process has started @{getCurrentTimeString()}")

    airtest = Process(
        target=hum.changeAir, args=())
    airtest.start()
    

    # Init Variables
    samplingTime = 20
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

    # Main Loop which will control all regulations
    loopGen = loop(samplingTime)
    liveDataLock = Lock()

    time.sleep(3)

    processes_NTD = []

    while(True):
        start = time.perf_counter()
        print(f"Loop has repeated @{getCurrentTimeString()}")
        # Active Climate: Loads Setpoints for Regulation
        activeClimate = loadClimate()
        phase = activeClimate.growPhase.phase

        # Processes Needed For Regulations: Sensors
        # Sensors
        oldTemp = temperature.value
        oldHum = humidity.value
        oldSoil = soilMoisture.value
        readSensors(temperature, humidity, soilMoisture, liveDataLock)

        # Regulations
        tempSetpoint = float(activeClimate.getTemperature(phase=phase))
        humSetpoint = float(activeClimate.getHumidity(phase=phase))

        processes_Regulations = [temperatureRegulation(
            temperature, oldTemp, tempSetpoint), humidityRegulation(humidity, oldHum, humSetpoint)]

        # Wait for all Processes to finish
        for pr in processes_Regulations:
            pr.join()

        processes_Regulations = []

        # Processes not Time Dependended: Lamp, LiveData Update in Firebase, Irrigation(once a day)
        processes_NTD = [
            lamp(activeClimate.getSuntime(phase)), updateLiveData(temperature, humidity, soilMoisture,
                                                                  growProgress, waterTankLevel, liveDataLock, token)]

        # Irrigation
        if(irrigationTime.day != datetime.now().day):
            irrigationTime = irrigationTime.replace(day=datetime.now().day)
            irrigated = False
        if(irrigationTime.hour == datetime.now().hour and irrigated == False):
            processes_NTD.append(irrigation())
            irrigated = True

        # Wait for all Processes to finish
        for pr in processes_NTD:
            pr.join()

        end = time.perf_counter()
        print(f"Time:  {end-start} ")

        processes_NTD = []
        print(getCurrentTimeString())
        loopGen.__next__()


def shutdown():
    print(shutdown)


def lamp(suntime):
    lamp_Process = Process(
        target=light.sunTimeChanged, args=(suntime, suntime))
    lamp_Process.start()
    return lamp_Process


def temperatureRegulation(temperature, old_temperature, tempSetpoint):
    temp_process = Process(
        target=tr.temperatureRegulationCycle, args=(temperature.value, old_temperature, tempSetpoint))
    temp_process.start()
    return temp_process


def humidityRegulation(humidity, old_humidity, humSetpoint):
    hum_process = Process(
        target=hum.humidityRegulationCycle, args=(humidity.value, old_humidity, humSetpoint))
    hum_process.start()
    return hum_process


def irrigation(amount, percentage):
    irrigation_Process = Process(
        target=ir.irrigationStart, args=(amount, percentage))
    irrigation_Process.start()
    irrigation_Process.join()

    print()


def updateLiveData(temperature, humidity, soilMoisture, growProgress, waterTankLevel, liveDataLock, token):
    liveDataProcess = Process(
        target=db.updateLiveData, args=(temperature, humidity, soilMoisture, growProgress, waterTankLevel, liveDataLock, token))
    liveDataProcess.start()
    return liveDataProcess


def loadClimate():
    existing_shm = shared_memory.SharedMemory(
        name='activeClimate')

    buffer = existing_shm.buf
    json = buffer[:].tobytes().decode()
    climate = db.Climate(json)

    print(f"Active Climate has been loaded @{getCurrentTimeString()}")
    return climate


def readSensors(temperature, humidity, soilMoisture, lock):

    sensors_process = Process(
        target=sensors.readValues, args=(temperature, humidity, soilMoisture, lock), daemon=True)
    sensors_process.start()
    print(f"Sensors Process has started @{getCurrentTimeString()}")
    sensors_process.join()
    print(f"Sensors Process has finished @{getCurrentTimeString()}")
    return temperature.value, humidity.value, soilMoisture.value,


def getCurrentTimeString():
    now = datetime.now()
    return now.strftime("%d.%m.%Y %H:%M:%S")


if __name__ == "__main__":
    main()
