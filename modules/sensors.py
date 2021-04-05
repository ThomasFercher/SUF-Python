import board
import adafruit_dht

from multiprocessing import shared_memory
import modules.adc as adc

# DHT22
pin = board.D21
dhtDevice = adafruit_dht.DHT22(pin)


def readValues(temperature, humidity, soilMoisture, lock):
    temp, hum = readDHT()
    soil = readSoilMoisture()
    with lock:
        temperature.value = temp
        soilMoisture.value = hum
        soilMoisture.value = soil
    print(
        f"Temperature:{temperature} Humidity:{humidity} SoilMoisture:{soilMoisture}  @12")


def readDHT():
    try:
        # Print the values to the serial port
        temperature = dhtDevice.temperature
        humidity = dhtDevice.humidity
       
        return temperature, humidity

    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])

    except Exception as error:
        dhtDevice.exit()
        raise error


def readSoilMoisture():
    val = adc.readADC()
    print(f"Soil Moisture: {val}%")
    return val