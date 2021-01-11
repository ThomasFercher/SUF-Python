from simple_pid import PID
import sensors


pid = PID(1, 0.1, 0.05, setpoint=1,sample_time=0.1,)

def setSetpoint(value):
    pid.setpoint = value
    

# assume we have a system we want to control in controlled_system
v = 1
pid.sample_time = 0.01

while True:
    v = readValue()
    # compute new ouput from the PID according to the systems current value
    control = pid(v)

    # feed the PID output to the system and get its current value
    v = control
    print(v)