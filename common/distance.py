class Distance:

    def __init__(self, distance, time):
        self.distance = distance
        self.time = time

    def __str__(self):
        return str(self.distance) + " " + str(self.time)
