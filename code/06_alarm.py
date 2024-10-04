from machine import Pin, ADC
from time import sleep
import network
import requests
import json

WLAN_SSID = 'ssid'
WLAN_PSK = 'password'

API_URI = 'https://api.example.com/alarm'
API_AUTH = 'Bearer xxxx'
API_GROUP = 'abcd1234'

WATER_THRES = 1000
HUM_THRES = 70


def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print(f"Connecting to network {WLAN_SSID!r}...")
        wlan.connect(WLAN_SSID, WLAN_PSK)
        while not wlan.isconnected():
            sleep(0.1)
        print("network config:", wlan.ifconfig())


def alarm(state):
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': API_AUTH,
    }
    data = {
        'groups': [API_GROUP],
        'alarm': {
            'title': "Test",
            "alarm_details": {
                'texts': [str(state)],
            }
        }
    }
    print(f"Sending alarm: {data}")
    r = requests.post(API_URI, data=json.dumps(data).encode(), headers=headers)
    if r.status_code == 200:
        alarm_id = r.json()['alarm_id']
        print(f"Alarm sent: {alarm_id=}")
    else:
        print(f"Error sending alarm: {r.json()}")


def weather(sensor):
    sensor.measure()
    temp = sensor.temperature()
    hum = sensor.humidity()
    return temp, hum


water_sensor = ADC(Pin(1), atten=ADC.ATTN_11DB)
dht22 = dht.DHT22(Pin(4, Pin.IN, Pin.PULL_UP))

while True:
    water_value = water_sensor.read_u16()
    _, hum = weather(dht22)
    if water_value > WATER_THRES:
        alarm(f"Wasser: {water_value}")
        sleep(100)
    elif hum > HUM_THRES:
        alarm(f"Luftfeuchte: {hum}")
        sleep(100)
    sleep(0.1)
