import sys
import os

# allow tests to import from the twin/ package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from twin.battery import Battery


def test_battery_starts_full():
    battery = Battery(capacity=100)
    assert battery.level == 100


def test_consume_reduces_level():
    battery = Battery(capacity=100)
    battery.consume(20)
    assert battery.level == 80


def test_consume_cannot_go_negative():
    battery = Battery(capacity=100)
    battery.consume(150)
    assert battery.level == 0


def test_charge_increases_level():
    battery = Battery(capacity=100)
    battery.consume(50)
    battery.charge(10)
    assert battery.level == 60


def test_charge_cannot_exceed_capacity():
    battery = Battery(capacity=100)
    battery.charge(9999)
    assert battery.level == 100


def test_is_critical_below_threshold():
    battery = Battery(capacity=100)
    battery.consume(90)
    assert battery.is_critical() is True


def test_is_not_critical_above_threshold():
    battery = Battery(capacity=100)
    assert battery.is_critical() is False