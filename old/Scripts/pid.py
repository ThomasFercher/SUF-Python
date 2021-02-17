from simple_pid import PID
import threading, time
import sensors


pid = PID(1, 0.1, 0.05, setpoint=30,sample_time=0.1,)

def setSetpoint(value):
    pid.setpoint = value
    

# assume we have a system we want to control in controlled_system
temperature = 30
old_temperature = 30;
pid.sample_time = 1

ta = pid.sample_time

def do_every(period,f):
    def g_tick():
        t = time.time()
        while True:
            t += period
            yield max(t - time.time(),0)
    g = g_tick()
    while True:
        time.sleep(next(g))
        f()

def cycle():
	global temperature
	old_temperature = temperature
	
	dht = sensors.readDHT()
	if not(dht is None):
		temperature,humidity = sensors.readDHT()
	else:
		temperature = old_temperature
    # compute new ouput from the PID according to the systems current value
	control = pid(temperature)

    # feed the PID output to the system and get its current value
    
  
	print(control)
	print(temperature)


while True:
	cycle()
	time.sleep(1)


