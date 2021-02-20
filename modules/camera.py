from datetime import datetime
import time
from typing import TYPE_CHECKING

import modules.database as db

# initialize the camera and grab a reference to the raw camera capture
#camera = PiCamera()
#camera.rotation = 180
#rawCapture = PiRGBArray(camera)


fileName = "photo"
path = "../images/"


def takePhoto():
    ts = datetime.now()
    date = ts.strftime("%Y-%m-%d %H:%M:%S")
    name = fileName+"_"+date+".jpg"

    # take Image and save it
    time.sleep(0.5)
    # camera.capture(path+name)
    time.sleep(0.5)

    name = "2021-02-20 15.05.32.jpg"
    path = "modules\images\\"

    return path, name, date
