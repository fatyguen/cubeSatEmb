import random

class CPU:
    def __init__(self, idle_temp=35, max_temp=80):
        self.idle_temp = idle_temp
        self.max_temp = max_temp
        self.temperature = idle_temp
        self.load = 10

    def tick(self):
        self.load = max(0, min(100, self.load + random.randint(-5, 8)))
        target_temp = self.idle_temp + (self.load * 0.5)
        self.temperature += (target_temp - self.temperature) * 0.3

    def is_overheating(self):
        return self.temperature >= self.max_temp

    def status(self):
        return f"CPU: {self.temperature:.1f}C, load {self.load}%"