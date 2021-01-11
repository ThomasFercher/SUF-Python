from simple_pid import PID
import threading, time


pid = PID(1, 0.1, 0.05, setpoint=1,sample_time=0.1,)

def setSetpoint(value):
    pid.setpoint = value
    

# assume we have a system we want to control in controlled_system
v = 1
pid.sample_time = 1

ta = pid.sample_time

def do_every(period,f,*args):
    def g_tick():
        t = time.time()
        while True:
            t += period
            yield max(t - time.time(),0)
    g = g_tick()
    while True:
        time.sleep(next(g))
        f(*args)

def cycle():
    temperature,humidity = readDHT()
    # compute new ouput from the PID according to the systems current value
    control = pid(temperature)

    # feed the PID output to the system and get its current value
    
    print('{} ({:.4f})'.format(s,time.time()))
    print(control)
    print(temperature)




do_every(ta,cycle)

