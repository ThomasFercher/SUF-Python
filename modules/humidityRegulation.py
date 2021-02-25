from simple_pid import PID
import gpiozero
from gpiozero import PWMOutputDevice
from time import sleep

ta = 10
kp = 1
ki = 0.1
kd = 0.05
global pid
pid = PID(kp, ki, kd, setpoint=30, sample_time=ta)
pid.Kp = kp


abluft =PWMOutputDevice(pin=18,active_high=True, initial_value=0,frequency=100)


def humidityRegulationCycle(humidity, old_humidity, setpoint):
    print(f"Temperature={humidity} Old Value={old_humidity}")
    print(f"Setpoint={setpoint}")

    control = pid(humidity)

    print(f"Control={control}")


def changeAir():


    abluft.on()
    #servo.openValve()
    sleep(20)

    
    #servo.closeValve()
    abluft.off()
