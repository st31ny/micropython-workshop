from machine import Pin, ADC
from time import sleep

# Konstante für Schwellwert
WATER_THRES = 1000

# definiere Funktion mit einem Parameter led
def alarm_blink(led):
    for _ in range(10):
        led.value(not led.value())
        sleep(0.2)

water_sensor = ADC(Pin(1), atten=ADC.ATTN_11DB)
led = Pin(8, Pin.OUT)
led.value(1)

while True:
    water_value = water_sensor.read_u16()
    if water_value > WATER_THRES:
        # gebe Warnung mit aktuellem Wasserstand aus
        print(f"Wasser erkannt: {water_value}")
        # rufe Funktion `alarm_blink()` auf
        alarm_blink(led)
        sleep(5)
    sleep(0.1)
