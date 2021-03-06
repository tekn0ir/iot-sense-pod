from threading import Lock
import paho.mqtt.client as mqtt
import datetime
import json
import rainbow
from timeloop import Timeloop
from datetime import timedelta
from sense_hat import SenseHat
import os
import logging
import sys

logger = logging.getLogger('iot-sense')
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.INFO)

logger.info("TΞꓘN01R")
logger.info("TΞꓘN01R")
logger.info("TΞꓘN01R")
logger.info("TΞꓘN01R")

message = os.getenv("IOT_SENSE_MSG", "TEKNOIR")
color = (255, 0, 35) # RED
client = mqtt.Client("iot-sense")

sense = SenseHat()
sense.set_rotation(180)
sense.clear()

animate_lock = Lock()

def error_str(rc):
    return '{}: {}'.format(rc, mqtt.error_string(rc))

def on_connect(_client, _userdata, _flags, rc):
    logger.info('Connected to internal broker {}'.format(error_str(rc)))

# def on_publish(_client, _userdata, _mid):
#     logger.info('on_publish')

def on_message(_client, _userdata, msg):
    payload = msg.payload.decode("utf-8","ignore")
    logger.info('Received on topic \'{}\' payload \'{}\' '.format(msg.topic, payload))
    parsed_json = json.loads(payload)
    logger.info('Parsed: \'{}\''.format(parsed_json))
    if 'color' in parsed_json:
        logger.info('Color: \'{}\''.format(color))
        global color
        c = parsed_json.get('color', {'r': 0, 'g': 0, 'b': 0})
        color = (c.get('r', 0), c.get('g', 0), c.get('b', 0))
    if 'message' in parsed_json:
        global message
        message = parsed_json.get('message')
        logger.info('Message: \'{}\''.format(message))
        with animate_lock:
            sense.show_message(message, text_colour=color)

client.on_connect = on_connect
# client.on_publish = on_publish
client.on_message = on_message

client.connect(os.getenv("HMQ_SERVICE_HOST", "hmq.kube-system"), os.getenv("HMQ_SERVICE_PORT", 1883))
client.subscribe("toe/commands/iot-sense/#", qos=1)
client.loop_start()  # This runs the network code in a background thread and also handles reconnecting for you.

tl = Timeloop()

@tl.job(interval=timedelta(seconds=2))
def sample_sensors_every_2s():
    temperature = sense.get_temperature()
    humidity = sense.get_pressure()
    pressure = sense.get_humidity()
    dir = sense.get_compass()
    payload = '{{ "ts": "{}", "temperature": {}, "pressure": {}, "humidity": {}, "compass": {} }}'.format(datetime.datetime.now().isoformat(), temperature, pressure, humidity, dir)
    logger.info(payload)
    client.publish("toe/events", payload)

@tl.job(interval=timedelta(seconds=0.002))
def animation():
    with animate_lock:
        for pix in rainbow.pixels:
            rainbow.next_colour(pix)
        sense.set_pixels(rainbow.pixels)

tl.start(block=True)
sense.clear()
