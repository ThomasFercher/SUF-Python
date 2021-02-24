import json


class LiveData(object):

    def __init__(self, temperature, humidity, soilMoisture, waterTankLevel, growProgress):
        self.temperature = temperature
        self.humidity = humidity
        self.soilMoisture = soilMoisture
        self.waterTankLevel = waterTankLevel
        self.growProgress = growProgress

    def getJson(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class GrowPhase(object):

    def __init__(self, data, empty=False):
        if empty is True:
            self.name = None
        else:
            self.__dict__ = data
            self.phase = data["phase"]
            self.flower_hum = data["flower_hum"]
            self.flower_suntime = data["flower_suntime"]
            self.flower_temp = data["flower_temp"]
            self.lateflower_hum = data["lateflower_hum"]
            self.lateflower_suntime = data["lateflower_suntime"]
            self.lateflower_temp = data["lateflower_temp"]
            self.vegetation_hum = data["vegation_hum"]
            self.vegetation_suntime = data["vegation_suntime"]
            self.vegetation_temp = data["vegation_temp"]

    def get_buffer(self):

        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4).encode()


class Climate(object):
    def __init__(self, data, empty=False):

        if data != None or len(data) != 0:
            data = data.replace('\x00', '')
            datasep = data.split("}", 2)
            try:
                data = datasep[0]+"}"+datasep[1]+"}"
            except:
                print()

        if empty == True or data == '':
            self.name = None
        else:

            self.__dict__ = json.loads(data)
            self.automaticWatering = self.__dict__["automaticWatering"]
            self.id = self.__dict__["id"]
            self.name = self.__dict__["name"]
            self.soilMoisture = self.__dict__["soilMoisture"]
            self.waterConsumption = self.__dict__["waterConsumption"]
            self.growPhase = GrowPhase(self.__dict__["growPhase"])

    def get_buffer(self):

        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4).encode('utf-8')

    def getTemperature(self, phase):
        if phase == "vegetation":
            return self.growPhase.vegetation_temp
        elif phase == "flower":
            return self.growPhase.flower_temp
        elif phase == "lateflower":
            return self.growPhase.lateflower_temp
        else:
            return 0.0

    def getHumidity(self, phase):
        if phase == "vegetation":
            return self.growPhase.vegetation_hum
        elif phase == "flower":
            return self.growPhase.flower_hum
        elif phase == "lateflower":
            return self.growPhase.lateflower_hum
        else:
            return 0.0

    def getSuntime(self, phase):
        if phase == "vegation":
            return self.growPhase.vegetation_suntime
        elif phase == "flower":
            return self.growPhase.flower_suntime
        elif phase == "lateflower":
            return self.growPhase.lateflower_suntime
       
