# CubeSat Digital Twin

A Python simulation of a CubeSat's core subsystems — battery, CPU, and temperature
sensor — with a mode state machine (NORMAL, LOW POWER, SAFE MODE, SHUTDOWN) and
randomized fault injection (sensor failures, CPU thermal spikes, communication
timeouts), all logged to file and console.

## Why this project

Real embedded and aerospace systems are built around managing sensors, state,
faults, and telemetry under real-world constraints. This project simulates
that kind of system: components tick forward in time, faults are injected
and recover on their own, and the satellite transitions between operational
modes based on live conditions — just like firmware managing a real spacecraft.

## Features
- Battery, CPU, and temperature sensor simulation
- State machine: NORMAL → LOW POWER → SAFE MODE → SHUTDOWN
- Randomized fault injection with automatic recovery
- Structured logging to console and `logs/system.log`
- Configuration driven by `config/config.yaml` (no hardcoded values)

## Run it
python -m venv .venv
.venv\Scripts\activate      # Windows
pip install -r requirements.txt
python main.py

## Roadmap
- [x] Battery, CPU, sensor simulation
- [x] Mode state machine
- [x] Fault injection system
- [ ] Unit tests
- [ ] Live dashboard
- [ ] Telemetry history / plotting