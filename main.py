from simple import MQTTClient
import os
import gc
import sys
from time import sleep_ms

# Imports required by MFRC522
from machine import Pin, SPI
from mfrc522 import MFRC522

# Define pins
sck, mosi, miso = Pin(18, Pin.OUT), Pin(23, Pin.OUT), Pin(19, Pin.OUT)
spi = SPI(baudrate=100000, polarity=0, phase=0, sck=sck, mosi=mosi, miso=miso)
sda = Pin(5, Pin.OUT)

# create a random MQTT clientID 
random_num = int.from_bytes(os.urandom(3), 'little')
mqtt_client_id = bytes('client_'+str(random_num), 'utf-8')

ADAFRUIT_IO_URL = b'io.adafruit.com' 
ADAFRUIT_USERNAME = b''
ADAFRUIT_IO_KEY = b''
ADAFRUIT_IO_FEEDNAME = b'rfid'

client = MQTTClient(client_id=mqtt_client_id, 
                    server=ADAFRUIT_IO_URL, 
                    user=ADAFRUIT_USERNAME, 
                    password=ADAFRUIT_IO_KEY,
                    ssl=False)

def connect():
    try:            
        client.connect()
    except:
        print('could not connect to MQTT server')
        sys.exit()

#   "ADAFRUIT_USERNAME/feeds/ADAFRUIT_IO_FEEDNAME"
mqtt_feedname = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, ADAFRUIT_IO_FEEDNAME), 'utf-8')

def do_read():
    try:
        connect()
        while True:
            print('readin')
            rdr = MFRC522(spi, sda)
            uid = ""
            (stat, _) = rdr.request(rdr.REQIDL)
            if stat == rdr.OK:
                (stat, raw_uid) = rdr.anticoll()
                if stat == rdr.OK:
                    uid = ("0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
                    print(uid)
                    client.publish(mqtt_feedname, bytes(str(uid),'utf-8'), qos=0)
                    sleep_ms(5000)
                    gc.collect()
    except:
        print('error')
        sys.exit()
