import random

class TemperatureSensor:
    def __init__(self):
        self.working = True
        self.last_reading = 20.0

    def read(self):
        if not self.working:
            return None
        # small chance the sensor fails this tick
        if random.random() < 0.02:
            self.working = False
            return None
        noise = random.uniform(-1.5, 1.5)
        self.last_reading += noise
        return round(self.last_reading, 2)

    def repair(self):
        self.working = True