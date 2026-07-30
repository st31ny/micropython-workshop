import machine
import time

led = machine.Pin(8, machine.Pin.OUT)
sensor = machine.Pin(10, machine.Pin.IN)

state = 0
while True:
    if sensor.value():
        led.value(0)
        if state == 0:
            print("Bewegung erkannt!")
            state = 1
    else:
        led.value(1)
        if state == 1:
            print("Bewegung gestoppt!")
            state = 0
    time.sleep(0.1)
