class Coordinates:

    def __init__(self, lat, log):
        self.lat = lat
        self.log = log

    def __str__(self):
        return str(self.lat) + "," + str(self.log)
