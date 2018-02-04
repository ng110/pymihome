"""
pymihome

Neil Griffin 
31st January 2018

"""
import requests
from requests.auth import HTTPBasicAuth
import json
from sys import getsizeof

HEADER_T = {'content-type':'application/json'}
BASEURL = "https://mihome4u.co.uk/api/v1/"
LISTSUBDEVICES = BASEURL + "device_groups/list"
FETCHUSAGEDATA = BASEURL + "subdevices/get_data"
DEVICEINFO = BASEURL + "subdevices/show"
POWERON = BASEURL + "subdevices/power_on"
POWEROFF = BASEURL + "subdevices/power_off"

class EnergenieTypeError(Exception):
    pass

class Connection():

    def __init__(self, username, key, logger=None):
        self._logger = logger
        self._auth = HTTPBasicAuth(username, key)
        _data = self.post(LISTSUBDEVICES)
        self._subdevices = _data[0]["subdevices"]
        for dev in self._subdevices:
            dtype = dev["device_type"]
            if dtype == 'control' dtype == 'legacy' or dtype == 'socket':
                dev['is_switch'] = True
            else:
                dev['is_switch'] = False
            if dtype == 'control' dtype == 'house':
                dev['is_sensor'] = True
            else:
                dev['is_sensor'] = False
#        self.devicelookup = {}
#        for i, subdevice in enumerate(self.subdevices):
#            print(i, self.subdevices[i]["id"], self.subdevices[i]["label"], 'type:',
#                  self.subdevices[i]["device_type"], flush=True)
#            self.devicelookup[subdevice["label"]] = subdevice

    def post(self, method, id=None):
        if id:
            response = requests.post(method, auth=self._auth,
                                     data=json.dumps({"id":id}),
                                     headers=HEADER_T)
        else:
            response = requests.post(method, auth=self._auth)
        print(getsizeof(response))
        response_d = response.json()
        if response_d['status'] != 'success':
            self._success = False
            return False
        self._success = True
        return response_d['data']

    @property
    def is_valid_login(self):
        return self._success

    @property
    def subdevices(self):
        return self._subdevices


class EnergenieSensor():
    def __init__(self, mihome, subdevice):
        self._name = subdevice["label"]
        self._type = subdevice["device_type"]  # control, legacy, socket, ecalm, etrv, house
        self._is_sensor = subdevice["is_sensor"]
        self._id = subdevice["id"]
        self._devid = subdevice["device_id"]
        if not self._is_sensor:
            raise EnergenieTypeError("Type '{}' is not a known sensor".format(self._type))

    @property
    def name(self):
        return self._name

    @property
    def power(self):
        data = self.mihome.post(DEVICEINFO, self._id)
        return bool(data['real_power'])
#        return bool(data['last_data_instant])

    @property
    def todays_usage(self):
        data = self.mihome.post(DEVICEINFO, self._id)
        return bool(data['today_wh'])

    @property
    def voltage(self):
        data = self.mihome.post(DEVICEINFO, self._id)
        return bool(data['voltage'])



class EnergenieSwitch():
    def __init__(self, mihome, subdevice):
        self._name = subdevice["label"]
        self._type = subdevice["device_type"]  # control, legacy, socket, ecalm, etrv, house
        self._is_switch = subdevice["is_switch"]
        self._id = subdevice["id"]
        self._devid = subdevice["device_id"]
        if not self._is_switch:
            raise EnergenieTypeError("Type '{}' is not a known switch".format(self._type))

    @property
    def name(self):
        return self._name

    def turn_on(self):
        return bool(self.mihome.post(POWERON, self._id))

    def turn_off(self):
        return bool(self.mihome.post(POWEROFF, self._id))

    @property
    def is_monitor(self):
        if self._type == 'control':
            return True
        return False

    @property
    def is_sensor(self):
        if self._type == 'control' or self._type == 'house':
            return True
        return False

    @property
    def state(self):
        if self.is_monitor:
            data = self.mihome.post(DEVICEINFO, self._id)
            return bool(data['power_state'])

    @property
    def power(self):
        if self.is_sensor:
            data = self.mihome.post(DEVICEINFO, self._id)
            return bool(data['real_power'])
#            return bool(data['last_data_instant])

    @property
    def todays_usage(self):
        if self.is_sensor:
            data = self.mihome.post(DEVICEINFO, self._id)
            return bool(data['today_wh'])

    @property
    def voltage(self):
        if self.is_sensor:
            data = self.mihome.post(DEVICEINFO, self._id)
            return bool(data['voltage'])


if __name__ == '__main__':
    print('pymihome.py')
