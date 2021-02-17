# Main Function of the SUF Script
# use command to start: python3 main.py >> output.txt
import time
from multiprocessing import Process, Pipe
from datetime import datetime
from modules.loop import loop
import time
import modules.database as db

samplingTime = 10


def getCurrentTimeString():
    now = datetime.now()
    return now.strftime("%d.%m.%Y %H:%M:%S")


def main():
    print(f"SUF-Box Script has started @{getCurrentTimeString()}")

    db.init()

    firebase_p, firebase_c = Pipe()
    firebase_process_parent = Process(
        target=firebase_main, args=(firebase_p, ))
    firebase_process_child = Process(
        target=firebase_child, args=(firebase_c, ))
    firebase_process_child.start()
    firebase_process_parent.start()

    print(firebase_p.recv())
    print(firebase_c.recv())
    firebase_process_child.join()
    firebase_process_parent.join()
    # loopGen = loop(samplingTime)  # Planning to wake up each 3 seconds
    # loopGen.__next__()
    # print(getCurrentTimeString())


def firebase_main(main):
    ''' This function sends the data for the child process '''
    main.send(['Hello'])
    main.close()


def firebase_child(child):
    ''' This function sends the data for the parent process '''
    child.send(['Bye'])
    child.close()


def accurate_delay(delay):
    ''' Function to provide accurate time delay in millisecond
    '''
    _ = time.perf_counter() + delay/1000
    while time.perf_counter() < _:
        pass


if __name__ == "__main__":
    main()
