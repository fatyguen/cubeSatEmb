import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from twin.cpu import CPU


def test_cpu_starts_at_idle_temperature():
    cpu = CPU(idle_temp=35, max_temp=80)
    assert cpu.temperature == 35


def test_cpu_not_overheating_at_start():
    cpu = CPU(idle_temp=35, max_temp=80)
    assert cpu.is_overheating() is False


def test_cpu_is_overheating_above_max():
    cpu = CPU(idle_temp=35, max_temp=80)
    cpu.temperature = 85
    assert cpu.is_overheating() is True


def test_cpu_load_stays_within_bounds():
    cpu = CPU(idle_temp=35, max_temp=80)
    for _ in range(200):
        cpu.tick()
        assert 0 <= cpu.load <= 100