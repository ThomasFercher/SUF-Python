import json


class LiveClimate(object):

    def __init__(self, temperature, humidity, soilMoisture, waterTankLevel, growProgress):
        self.temperature = temperature
        self.humidity = humidity
        self.soilMoisture = soilMoisture
        self.waterTankLevel = waterTankLevel
        self.growProgress = growProgress

    def getJson(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
