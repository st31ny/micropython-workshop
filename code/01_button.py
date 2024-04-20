# importiere Pin-Klasse auf machine-Modul
from machine import Pin
# importiere sleep-Funktion aus time-Modul
from time import sleep

# instanziiere Pin-Klasse für Pin 8 als Ausgang
led = Pin(8, Pin.OUT)
# instanziiere Pin-Klasse für Pin 0 als Eingang mit Pull-Up-Widerstand
button = Pin(0, Pin.IN, Pin.PULL_UP)
# lese aktuellen Wert vom Button (0 oder 1)
button_value = button.value()

while True:
    button_value_new = button.value()
    if button_value_new == 1 and button_value == 0:
        # Flanke erkannt! => schalte LED um
        led.value(not led.value())
    button_value = button_value_new
    # warte 100 ms
    sleep(0.1)