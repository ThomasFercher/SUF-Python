from simple_pid import PID

ta = 10
kp = 1
ki = 0.1
kd = 0.05
global pid
pid = PID(kp, ki, kd, setpoint=30, sample_time=ta)
pid.Kp = kp


def humidityRegulationCycle(humidity, old_humidity, setpoint):
    print(f"Temperature={humidity} Old Value={old_humidity}")
    print(f"Setpoint={setpoint}")

    control = pid(humidity)

    print(f"Control={control}")
