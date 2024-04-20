from machine import Pin
from time import sleep

led = Pin(8, Pin.OUT)
while True:
    led.value(not led.value())
    print(f"LED ist {led.value()}")
    sleep(0.5)