from network import WLAN
from mqtt import MQTTClient
import time
import pycom
import json

### Settings, adjust as required for your case!
MQTT_BROKER_ADDRESS = ''
MQTT_BROKER_PORT = 1883
MQTT_CONTROL_TOPIC = 'pycom/light/set'
###


# Wait intil device is connected
while not wlan.isconnected():
     machine.idle()

# Add here the
client = MQTTClient("pycom", MQTT_BROKER_ADDRESS, port=MQTT_BROKER_PORT)
client.settimeout = 5

class Light():
    """The RGB light on the Pycom board
    """

    def __init__(self, state_on=False, brightness=0, r=255, g=255, b=255):
        self.brightness = brightness
        self.r = r
        self.g = g
        self.b = b
        self.state_on = state_on
        self.last_brightness = 255

    def set_brightness(self, brightness):
        """Set the brightness level (accepted: 0 <= brightness <= 255)
        """
        if brightness < 0:
            brightness = 0
        elif brightness > 255:
            brightness = 255
        self.brightness = brightness
        self.show()

    def set_color(self, r, g, b):
        """Show a specific R/G/B color
        """
        self.r = r
        self.g = g
        self.b = b
        self.show()

    def set_off(self):
        """Set the light off
        """
        if self.state_on:
            self.state_on = False
            self.last_brightness = self.brightness
            self.set_brightness(0)

    def set_on(self):
        """Turn the light on
        """
        if not self.state_on:
            self.set_brightness(self.last_brightness)
            self.state_on = True

    def show(self):
        """Actually set light values
        """
        scaled_r = int(self.r * self.brightness / 255)
        scaled_g = int(self.g * self.brightness / 255)
        scaled_b = int(self.b * self.brightness / 255)
        setcolor = scaled_r * 256 * 256 + scaled_g * 256 + scaled_b
        pycom.rgbled(setcolor)

# Set up light
light = Light()

def msg(topic, message):
    """Callback to handle incoming control message

    TODO: should also have a status channel to be consistent with Home Assistant dashboard
    """
    print(message)
    control = json.loads(message)
    if control['state'] == 'OFF':
        light.set_off()
    else:
        if len(control) > 1:
            if 'color' in control.keys():
                color = control['color']
                light.set_color(color['r'], color['g'], color['b'])
            if 'brightness' in control.keys():
                light.set_brightness(control['brightness'])
        else:
            light.set_on()

# MQTT setup
client.connect()
client.ping()
client.set_callback(msg)
client.subscribe(MQTT_CONTROL_TOPIC)

print("waiting")
while True:
    # Blocking call to receive a message
    client.wait_msg()
