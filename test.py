import modules.watering as ir
import modules.adc as adc
from multiprocessing import Process, shared_memory, Value, Lock


air = 20208
water = 9760

range = (air-water) / 100


def main():

    
    #irrigationTest()
    val = adc.readADC()
    print(val)
  


def irrigationTest():

    irtest = Process(
        target=ir.irrigationStart, args=(1.0, None))
    irtest.start()
    irtest.join()


main()
