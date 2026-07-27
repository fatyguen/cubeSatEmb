from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.live import Live

console = Console()

def build_dashboard(satellite, ext_temp):
    table = Table.grid(padding=(0, 2))
    table.add_column(justify="left", style="bold")
    table.add_column(justify="left")

    battery = satellite.battery
    cpu = satellite.cpu

    bar_length = 20
    filled = int((battery.level / battery.capacity) * bar_length)
    battery_bar = "█" * filled + "░" * (bar_length - filled)

    active_faults = [
        name for name, active in satellite.fault_manager.active_faults.items()
        if active
    ]
    faults_str = ", ".join(active_faults) if active_faults else "none"

    mode_color = {
        "NORMAL": "green",
        "LOW POWER": "yellow",
        "SAFE MODE": "red",
        "SHUTDOWN": "bright_red",
    }.get(satellite.mode, "white")

    table.add_row("Tick", str(satellite.tick_count))
    table.add_row("Mode", f"[{mode_color}]{satellite.mode}[/{mode_color}]")
    table.add_row("Battery", f"{battery_bar} {battery.level}%")
    table.add_row("CPU Temp", f"{cpu.temperature:.1f} C")
    table.add_row("CPU Load", f"{cpu.load}%")
    table.add_row("Ext Temp", f"{ext_temp} C" if ext_temp is not None else "OFFLINE")
    table.add_row("Comm", "OK" if satellite.comm_ok else "TIMEOUT")
    table.add_row("Active Faults", faults_str)

    return Panel(table, title="CubeSat Digital Twin", border_style="cyan")


def run_dashboard(satellite, update_fn, tick_delay):
    """
    update_fn should be a function that runs one satellite.update()
    and returns the ext_temp reading for that tick.
    """
    with Live(console=console, refresh_per_second=4) as live:
        while True:
            ext_temp = update_fn()
            live.update(build_dashboard(satellite, ext_temp))

            if satellite.mode == "SHUTDOWN":
                break

            import time
            time.sleep(tick_delay)