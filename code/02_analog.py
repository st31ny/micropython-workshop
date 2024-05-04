from machine import Pin, ADC, PWM
from time import sleep

# ADC mit 11 dB Dämpfung auf Pin 2 => 150mV..2450mV
pot = ADC(Pin(2), atten=ADC.ATTN_11DB)

# PWM mit 5 kHz auf Pin 8
led = PWM(Pin(8), freq=5000)

while True:
    # lese Wert des ADC (0..2**16)
    pot_val = pot.read_u16()
    # rechne um auf Duty-Cycle PWM (0..2**10)
    led_duty = pot_val / 2**6
    # konvertiere nach int und setze
    led.duty(int(led_duty))

    sleep(0.1)
