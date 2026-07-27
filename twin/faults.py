import random

class FaultManager:
    """
    Randomly injects and recovers faults across satellite subsystems.
    Each fault has a chance to trigger per tick, and a chance to
    resolve on its own once active (simulating recovery/retry logic).
    """

    def __init__(self, logger, fault_chance=0.03, recovery_chance=0.25):
        self.logger = logger
        self.fault_chance = fault_chance
        self.recovery_chance = recovery_chance

        # active faults are tracked by name -> True/False
        self.active_faults = {
            "sensor_failure": False,
            "cpu_spike": False,
            "comm_timeout": False,
        }

    def update(self, satellite):
        self._maybe_trigger("sensor_failure", satellite)
        self._maybe_trigger("cpu_spike", satellite)
        self._maybe_trigger("comm_timeout", satellite)

        self._maybe_recover("sensor_failure", satellite)
        self._maybe_recover("cpu_spike", satellite)
        self._maybe_recover("comm_timeout", satellite)

    def _maybe_trigger(self, fault_name, satellite):
        if self.active_faults[fault_name]:
            return  # already active, don't re-trigger

        if random.random() < self.fault_chance:
            self.active_faults[fault_name] = True
            self.logger.warning(f"FAULT TRIGGERED: {fault_name}")
            self._apply_fault(fault_name, satellite)

    def _maybe_recover(self, fault_name, satellite):
        if not self.active_faults[fault_name]:
            return  # nothing to recover from

        if random.random() < self.recovery_chance:
            self.active_faults[fault_name] = False
            self.logger.info(f"FAULT RECOVERED: {fault_name}")
            self._clear_fault(fault_name, satellite)

    def _apply_fault(self, fault_name, satellite):
        if fault_name == "sensor_failure":
            satellite.temp_sensor.working = False
        elif fault_name == "cpu_spike":
            satellite.cpu.temperature += 25
        elif fault_name == "comm_timeout":
            satellite.comm_ok = False

    def _clear_fault(self, fault_name, satellite):
        if fault_name == "sensor_failure":
            satellite.temp_sensor.repair()
        elif fault_name == "comm_timeout":
            satellite.comm_ok = True

    def any_active(self):
        return any(self.active_faults.values())