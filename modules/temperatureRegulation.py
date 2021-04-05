from simple_pid import PID
import gpiozero
from gpiozero import OutputDevice


petier =OutputDevice(pin=26,active_high=True, initial_value=False)
#heating = OutputDevice(pin=21,active_high=True, initial_value=False)





ta = 10
kp = 1
ki = 0.1
kd = 0.05
global pid
pid = PID(kp, ki, kd, setpoint=30, sample_time=ta)
pid.Kp = kp

#fan =OutputDevice(pin=15,active_high=True, initial_value=False)





def temperatureRegulationCycle(temperature, old_temperature, setpoint):
    print(f"Temperature={temperature} Old Value={old_temperature}")
    print(f"Setpoint={setpoint}")

    control = pid(temperature)

    if(setpoint-temperature>0.5 or setpoint-temperature<0.5):
        petier.on()
        print(f"Petier turned on")
    else:
        petier.off()
        print(f"Petier turned off")

    print(f"Control={control}")

    if(petier.is_active):
        if(control>0):
            #heating.on()
            print(f"Petier is heating")
        elif(control<0):
            #heating.off()   
            print(f"Petier is cooling") 

    
   
    

    
    


def turnPetier(p):

    print("Petier Power changed to {p}%")
    # GPIO = 123


