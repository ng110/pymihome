"""
pymihome

Neil Griffin
31st January 2018

"""
import requests
from requests.auth import HTTPBasicAuth
import json


HEADER_T = {'content-type': 'application/json'}
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
            if dtype == 'control' or dtype == 'legacy' or dtype == 'socket':
                dev['is_switch'] = True
            else:
                dev['is_switch'] = False
            if dtype == 'control' or dtype == 'house':
                dev['is_sensor'] = True
            else:
                dev['is_sensor'] = False
            if dtype == 'open':
                dev['is_binary'] = True
            else:
                dev['is_binary'] = False
#        self.devicelookup = {}
#        for i, subdevice in enumerate(self.subdevices):
#            print(i, self.subdevices[i]["id"], self.subdevices[i]["label"], 'type:',
#                  self.subdevices[i]["device_type"], flush=True)
#            self.devicelookup[subdevice["label"]] = subdevice

    def post(self, method, id=None):
        if id:
            response = requests.post(method, auth=self._auth,
                                     data=json.dumps({"id": id}),
                                     headers=HEADER_T)
        else:
            response = requests.post(method, auth=self._auth)
#        print(getsizeof(response))
        response_d = response.json()
#        print(response_d)
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


# Abstract base class
class EnergenieDevice():
    def __init__(self, mihome, subdevice):
        self._mihome = mihome
        self._name = subdevice["label"]
        self._type = subdevice["device_type"]  # control, legacy, socket, ecalm, etrv, house
        self._is_switch = subdevice["is_switch"]
        if self._type == 'control' or self._type == 'house':
            self._is_sensor = True
        else:
            self._is_sensor = False
        if self._type == 'open':
            self._is_binary = True
        else:
            self._is_binary = False
        self._id = subdevice["id"]
        self._devid = subdevice["device_id"]
        self.typecheck()
        self.getinfo()

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def is_sensor(self):
        return self._is_sensor

    @property
    def is_binary(self):
        return self._is_binary

    @property
    def is_switch(self):
        return self._is_switch

    def getinfo(self):
        self._data = self._mihome.post(DEVICEINFO, self._id)
        return bool(self._data)


class EnergenieBinary(EnergenieDevice):

    def typecheck(self):
        if not self._is_binary:
            raise EnergenieTypeError("Type '{}' is not a known binary sensor".format(self._type))

    @property
    def open(self):
        self.getinfo()
        return self._data['sensor_state'] == 1.0

    @property
    def closed(self):
        return not self.open


class EnergenieSensor(EnergenieDevice):

    def typecheck(self):
        if not self._is_sensor:
            raise EnergenieTypeError("Type '{}' is not a known sensor".format(self._type))

    @property
    def power(self):
        return self._data['real_power']
#        return self._data['last_data_instant]

    @property
    def realpower(self):
        return self._data['real_power']

    @property
    def lastpower(self):
        return self._data['last_data_instant']

    @property
    def todays_usage(self):
        return self._data['today_wh']

    @property
    def voltage(self):
        return self._data['voltage']



class EnergenieSwitch(EnergenieDevice):

    def typecheck(self):
        if not self._is_switch:
            raise EnergenieTypeError("Type '{}' is not a known switch".format(self._type))

    def turn_on(self):
        return bool(self._mihome.post(POWERON, self._id))

    def turn_off(self):
        return bool(self._mihome.post(POWEROFF, self._id))

    # @property
    # def is_monitor(self):
    #     if self._type == 'control':
    #         return True
    #     return False

    # @property
    # def is_sensor(self):
    #     if self._type == 'control' or self._type == 'house':
    #         return True
    #     return False

    @property
    def state(self):
        if self._is_sensor:
            return self._data['power_state']
        else:
            raise EnergenieTypeError

    @property
    def power(self):
        if self._is_sensor:
            return self._data['real_power']
        else:
            return None
#        return self._data['last_data_instant]

    @property
    def realpower(self):
        if self._is_sensor:
            return self._data['real_power']
        else:
            return None

    @property
    def lastpower(self):
        if self._is_sensor:
            return self._data['last_data_instant']
        else:
            return None

    @property
    def todays_usage(self):
        if self._is_sensor:
            return self._data['today_wh']
        else:
            return None

    @property
    def voltage(self):
        if self._is_sensor:
            return self._data['voltage']
        else:
            return None


if __name__ == '__main__':
    print('pymihome.py')
