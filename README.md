pymihome
===============================

version number: 0.0.7

author: Neil Griffin

Overview
--------

Library to access Energenie MiHome devices via the web API.

Work in progress.  Currently has some functionality, but limited and not
properly tested.  Use with care.

Installation / Usage
--------------------

To install use pip:

    $ pip install pymihome


Or clone the repo:

    $ git clone https://github.com/ng110/pymihome.git
    $ python setup.py install
    
Contributing
------------

Offers welcome, as I don't have much time to work on this!

License
-------

LGPLv3

Example
-------

    $ from pymihome import Connection, EnergenieSwitch

    $ mihome = Connection([username], [key|password])
    $ switches = [EnergenieSwitch(mihome, dev) for dev in mihome.subdevices if dev['is_switch']]
    $ for switch in switches:
    $     print(switch.name)

