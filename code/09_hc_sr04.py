import machine
import time

class HCSR04:
    # Klassenkonstanten
    _SOUND_SPEED = 0.34320 # mm/μs
    _MAX_RANGE = 4000 # mm

    def __init__(self, trigger_pin, echo_pin):
        # initialisiere Attribute des Objektes
        self._trigger = machine.Pin(trigger_pin, machine.Pin.OUT)
        self._trigger.value(0)
        self._echo = machine.Pin(echo_pin, machine.Pin.IN)

    def distance_mm(self):
        # Trigger-Pin sicher auf 0 ziehen
        self._trigger.value(0)
        time.sleep_us(5)
        # Impuls von 10 μs senden
        self._trigger.value(1)
        time.sleep_us(10)
        self._trigger.value(0)
        # Impulszeit messen
        timeout_us = 2 * self._MAX_RANGE / self._SOUND_SPEED
        pulse_time = machine.time_pulse_us(self._echo, 1, timeout_us)
        assert pulse_time > 0
        # Abstand berechnen
        return pulse_time * self._SOUND_SPEED / 2
    
sensor = HCSR04(trigger_pin=5, echo_pin=6)

while True:
    distance = sensor.distance_mm()
    print(f"Abstand: {distance*10:.1f} cm")
    time.sleep(1)
