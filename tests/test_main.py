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
    assert len(sensors) == 3, 'number of sensors'

def test_switch(mihome):
    sensors = [EnergenieSwitch(mihome, dev) for dev in mihome.subdevices if dev['is_switch']]
    assert len(sensors) == 7

def test_sensors(mihome):
    sensors = [EnergenieBinary(mihome, dev) for dev in mihome.subdevices if dev['is_binary']]
    assert len(sensors) == 1

