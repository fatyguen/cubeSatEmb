class Battery:
    def __init__(self, capacity=100):
        self.capacity = capacity
        self.level = capacity
        self.health = 100

    def consume(self, amount):
        self.level -= amount
        if self.level < 0:
            self.level = 0

    def charge(self, amount):
        self.level += amount
        if self.level > self.capacity:
            self.level = self.capacity

    def is_critical(self):
        return self.level <= 15

    def status(self):
        return f"Battery: {self.level}% (health {self.health}%)"