import csv
import os
from datetime import datetime

class TelemetryRecorder:
    """
    Records one row of telemetry per tick to a CSV file.
    Each mission run gets its own timestamped file so old
    runs are never overwritten.
    """

    def __init__(self, output_dir="logs/telemetry"):
        os.makedirs(output_dir, exist_ok=True)

        run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.filepath = os.path.join(output_dir, f"mission_{run_id}.csv")

        self.fieldnames = [
            "tick", "timestamp", "mode",
            "battery_level", "battery_health",
            "cpu_temp", "cpu_load",
            "ext_temp", "comm_ok",
            "active_faults"
        ]

        with open(self.filepath, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames)
            writer.writeheader()

    def record(self, satellite, ext_temp):
        active_faults = [
            name for name, active in satellite.fault_manager.active_faults.items()
            if active
        ]

        row = {
            "tick": satellite.tick_count,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "mode": satellite.mode,
            "battery_level": satellite.battery.level,
            "battery_health": satellite.battery.health,
            "cpu_temp": round(satellite.cpu.temperature, 2),
            "cpu_load": satellite.cpu.load,
            "ext_temp": ext_temp,
            "comm_ok": satellite.comm_ok,
            "active_faults": ";".join(active_faults) if active_faults else "none",
        }

        with open(self.filepath, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames)
            writer.writerow(row)