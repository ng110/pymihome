import pytest
import json
from os import path
from pymihome import Connection
from pymihome import EnergenieSensor, EnergenieBinary, EnergenieSwitch


@pytest.fixture(scope='session')
def mihome():
    here = path.abspath(path.dirname(__file__))
    with open(path.join(here, 'secrets.json'), 'r') as f:
        secrets = json.load(f)          # "enuser", "enkey", "hueuser", "hueip"
    mihome = Connection(secrets["enuser"], secrets["enkey"])
    yield(mihome)                       # after yeild is teardown code
    print('Teardown mihome connection.')


def test_sensors(mihome):
    sensors = [EnergenieSensor(mihome, dev) for dev in mihome.subdevices if dev['is_sensor']]
    print(len(sensors), 'sensors.')
    assert len(sensors) == 3, 'number of sensors'
    for sensor in sensors:
        print(sensor.name, flush=True)
        sensor.getinfo()
        assert sensor.is_sensor
        assert sensor.id
        assert type(sensor.power) is float
        assert type(sensor.name) is str


def test_switch(mihome):
    switches = [EnergenieSwitch(mihome, dev) for dev in mihome.subdevices if dev['is_switch']]
    print(len(switches), 'switches.')
    for switch in switches:
        print(switch.name)
    assert len(switches) == 13


def test_binaries(mihome):
    binaries = [EnergenieBinary(mihome, dev) for dev in mihome.subdevices if dev['is_binary']]
    print(len(binaries), 'binary sensors.')
    for binary in binaries:
        print(binary.name)
    assert len(binaries) == 1
