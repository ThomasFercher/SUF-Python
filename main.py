# Main Function of the SUF Script
# use command to start: python3 main.py >> output.txt
import time
from datetime import datetime

def getCurrentTimeString():
    now = datetime.now()
    return now.strftime("%d.%m.%Y %H:%M:%S")


     


def main():
    print(f"SUF-Box Script has started @{getCurrentTimeString()}")







def accurate_delay(delay):
    ''' Function to provide accurate time delay in millisecond
    '''
    _ = time.perf_counter() + delay/1000
    while time.perf_counter() < _:
        pass






if __name__ == "__main__":
    main()


