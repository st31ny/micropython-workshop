import dht
import machine
import time

pin = machine.Pin(4, machine.Pin.IN, machine.Pin.PULL_UP)
sensor = dht.DHT22(pin)

while True:
    sensor.measure()
    temp = sensor.temperature()
    hum = sensor.humidity()
    print(f"Temperatur: {temp}° C\nLuftfeuchte: {hum} %")
    time.sleep(2)