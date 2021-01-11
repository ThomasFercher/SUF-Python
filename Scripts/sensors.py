import board
import adafruit_dht

#DHT22
dhtDevice = adafruit_dht.DHT22(board.D18)

def readDHT():
   
	
	try:
		# Print the values to the serial port
		temperature = dhtDevice.temperature
		humidity = dhtDevice.humidity
		return temperature,humidity
	except RuntimeError as error:
		# Errors happen fairly often, DHT's are hard to read, just keep going
		print(error.args[0])
		
	except Exception as error:
		dhtDevice.exit()
		raise error
 
    
	