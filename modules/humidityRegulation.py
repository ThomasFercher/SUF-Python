from simple_pid import PID
import gpiozero
from gpiozero import PWMOutputDevice,OutputDevice
import modules.pump as pump
from time import sleep

ta = 10
kp = 1
ki = 0.1
kd = 0.05
global pid
pid = PID(kp, ki, kd, setpoint=30, sample_time=ta)
pid.Kp = kp

valve =OutputDevice(pin=17,active_high=True, initial_value=False)
abluft =OutputDevice(pin=20,active_high=True, initial_value=False)



def humidityRegulationCycle(humidity, old_humidity, setpoint):
    print(f"Temperature={humidity} Old Value={old_humidity}")
    print(f"Setpoint={setpoint}")

    control = pid(humidity)

    print(f"Control={control}")
    changeAir()

def squirt(duration,s):
    pump.turnOn()
    #valve.on()
    sleep(5)
    pump.turnOff()
    #valve.off()


def changeAir():
    abluft.on()
   
    
     
    #abluft.pulse(fade_in_time=10, fade_out_time=10, n=None, background=True)
    print(f"Fan Toggled")

   