# HomeAssistant - Pycom

Implementing a [Pycom](https://www.pycom.io/) board as a [MQTT JSON light](https://home-assistant.io/components/light.mqtt_json/)
for [Home Assistant](https://home-assistant.io). The onboard RGB LED is explosed
and can be controlled from the Home Assistant console.

*This is a work in progress!*

## Settings

In `boot.py` set your wifi credentials:

```Python
SSID = ''
WIFI_PASSWORD = ''
```

In `main.py` set your MQTT connection settings:

```Python
MQTT_BROKER_ADDRESS = ''
MQTT_BROKER_PORT = 1883
MQTT_CONTROL_TOPIC = 'pycom/light/set'
```

In Home Assistant's `configuration.yml` add your light (see more in the [docs](https://home-assistant.io/components/light.mqtt_json/)):

```YAML
light:
  - platform: mqtt_json
    name: Pycom
    command_topic: "pycom/light/set"
    brightness: true
    rgb: true
    retain: true
```

... and take it from here!

## License

Copyright 2017 Gergely Imreh <imrehg@gmail.com>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
