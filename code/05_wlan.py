from time import sleep
import network
import requests

WLAN_SSID = 'ssid'
WLAN_PSK = 'password'
WEATHER_URI = 'https://api.open-meteo.com/v1/forecast?latitude=48.01&longitude=10.03&hourly=temperature_2m&timezone=Europe%2FBerlin&forecast_days=1'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)


def connect_wifi():
    if not wlan.isconnected():
        print(f"Connecting to network {WLAN_SSID!r}...")
        wlan.connect(WLAN_SSID, WLAN_PSK)
        while not wlan.isconnected():
            sleep(0.1)
        print("network config:", wlan.ifconfig())


def get_weather():
    headers = {
        'Accept': 'application/json',
    }
    print(f"Requesting weather...")
    r = requests.get(WEATHER_URI, headers=headers)
    if r.status_code == 200:
        return r.json()
    else:
        print(f"Error getting weather: {r.json()}")


while True:
    connect_wifi()
    data = get_weather()
    if data:
        print("Wettervorhersage:")
        hourly = data['hourly']
        temp_unit = data['hourly_units']['temperature_2m']
        for time, temp in zip(hourly['time'], hourly['temperature_2m']):
            print(f"{time}\t{temp} {temp_unit}")
        sleep(1000)
    sleep(10)

