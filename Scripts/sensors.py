import board
import adafruit_dht

#DHT22
dhtDevice = adafruit_dht.DHT22(board.D18)

readDHT()

def readDHT():
    temperature = dhtDevice.temperature
    humidity = dhtDevice.humidity
    print(temperature)
    print(humidity)
    return temperature,humidity