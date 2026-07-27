from twin.battery import Battery
from twin.cpu import CPU
from twin.sensors import TemperatureSensor

class CubeSat:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.battery = Battery(capacity=config["battery_capacity"])
        self.cpu = CPU(
            idle_temp=config["cpu_idle_temp"],
            max_temp=config["cpu_max_temp"]
        )
        self.temp_sensor = TemperatureSensor()
        self.mode = "NORMAL"
        self.tick_count = 0

    def update(self):
        self.tick_count += 1

        # power
        self.battery.consume(self.config["battery_drain_per_tick"])
        self.battery.charge(self.config["solar_charge_per_tick"])

        # cpu
        self.cpu.tick()

        # sensor
        reading = self.temp_sensor.read()
        if reading is None:
            self.logger.warning("Temperature sensor offline")

        # state machine
        self._update_mode()

        # log a status line every tick
        self.logger.info(
            f"[tick {self.tick_count}] mode={self.mode} "
            f"{self.battery.status()} | {self.cpu.status()} | "
            f"ext_temp={reading}"
        )

    def _update_mode(self):
        if self.battery.level <= 0:
            self.mode = "SHUTDOWN"
        elif self.cpu.is_overheating():
            self.mode = "SAFE MODE"
        elif self.battery.is_critical():
            self.mode = "LOW POWER"
        else:
            self.mode = "NORMAL"