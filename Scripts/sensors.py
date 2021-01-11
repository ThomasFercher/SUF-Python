import Adafruit_DHT


#DHT22
sensor = Adafruit_DHT.DHT22
pin = '4'

def readValue():
    return Adafruit_DHT.read_retry(sensor, pin)