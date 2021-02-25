from simple_pid import PID


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
   
    print(f"Control={control}")


def turnPetier(p):

    print("Petier Power changed to {p}%")
    # GPIO = 123


