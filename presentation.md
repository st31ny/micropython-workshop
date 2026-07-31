---
marp: true
theme: default
class: invert
---

# Programmierung von Embedded Systems mit MicroPython

---

<!--
header: MicroPython
paginate: true
-->

## Agenda

1. Hello Universe
1. Grundlagen Sprache und IO
1. Digitale Sensoren und Aktoren
1. Netzwerk und Kommunikation
1. Projekt: Jetzt seid ihr am Zug!

---

# Hello Universe

Begriffe, Werkzeuge, Hello World

<!--
header: MicroPython: Hello Universe
-->

---

## Begriffe

- Microcontroller — ESP32
- Chip — Board
- Python — MicroPython

---

## Linkliste, Dokumentation, Präsentation

https://github.com/st31ny/micropython-workshop

---

## Werkzeuge

- Thonny: IDE für Python-Entwicklung mit MicroPython-Unterstützung
    - Download unter https://thonny.org
- ESP32-C3 SuperMini
    - dazu USB-Kabel, Sensoren, Breadboard
- 2er Gruppen oder allein mit einem Laptop und einem Bausatz

<!--
später: Messgerät, weitere Sensoren
-->

---

## Einrichtung

<!-- zeigen! -->
- Rechner per USB mit Chip verbinden
- Thonny starten
- Ersteinrichtung für MicroPython:
    - Werkzeuge > Optionen > Interpreter
    - Auswahl Interpreter: "MicroPython (ESP32)"
    - Auswahl Port
    - "OK"
- Kommandozeile: `help()`

---

## Dokumentation

- siehe Linkliste: https://github.com/st31ny/micropython-workshop
- MicroPython: https://docs.micropython.org
- Pinout: bei Händler oder im Netz suchen

---

![bg](https://www.nologo.tech/assets/img/esp32/esp32c3supermini/esp32c3foot1.png)

<!-- relevant sind die GPIO-Nummern -->

---

## Hello World

- Skriptbereich > Speichern > MicroPython device > "main.py"
- Eingabe:
```py
from machine import Pin
from time import sleep
led = Pin(8, Pin.OUT)
while True:
    led.value(not led.value())
    print("Hello World")
    sleep(1)
```
* Start per RST-Button
* zum Beenden: 🛑 (Strg+F2)

<!--
LED nochmal einzeln zeigen => Konzept Active Low vs. Active High
-->

---


# Grundlagen Sprache und IO

Buttons, LED, Radar, analoge Signale, Ultraschall

<!--
header: MicroPython: Grundlagen Sprache und IO
-->

---

## Buttonsteuerung

```py
from machine import Pin
from time import sleep

led = Pin(8, Pin.OUT)
button = Pin(0, Pin.IN, Pin.PULL_UP)
button_value = button.value()

while True:
    button_value_new = button.value()
    if button_value_new == 1 and button_value == 0:
        led.value(not led.value())
    button_value = button_value_new
    sleep(0.1)
```
<!--
Sprachkonstrukte:
* Import
* Funktion
* Objekt
* While-Schleife => grundlegende Programmstruktur
* If-Verzweigung (Bedingung, == Gleichheit)
* Zuweisung

Hardware:
* Button
* Was ist ein Pull-Up/Down?
-->

---

## Radar (1)

- funktioniert wie ein Button
- Anschlüsse beachten:
  - VIN — 5 V
  - GND — GND
  - OUT — GPIO (kein Pull-Up nötig)
  - andere Pins nicht belegen
* **TODO**: LED soll genau dann leuchten, wenn eine Bewegung erkannt wird
* **Bonus**: Text ausgeben, wenn der Zustand sich ändert

<!--
Hardware:
* Radarsensor
* 5 V Versorgung
-->

---

## Radar (2)

```py
# ...
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
```

---

## Potentiometer und Pulsweitenmodulation (1)

<!--
interne Referenzspannung 1.1 V
-->

- Messung von analogen Signalen per ADC
- Ausgabe von analogen Signalen per PWM

```py
from machine import Pin, ADC, PWM
from time import sleep

# ADC mit 11 dB Dämpfung auf Pin 2 => 150mV..2450mV
pot = ADC(Pin(2), atten=ADC.ATTN_11DB)
pot.read_u16() # gib Wert (0..65536)

# PWM mit 5 kHz auf Pin 8
led = PWM(Pin(0), freq=5000)
led.duty(512) # setze analogen Wert (0..1024)

# TODO: Dimme LED mit Poti.
```

<!--
Sprachkonstrukte:
* Kommentare
* benannte Parameter

Hardware:
* LED mit Vorwiderstand
-->

---

## Potentiometer und Pulsweitenmodulation (2)

```py
from machine import Pin, ADC, PWM
from time import sleep

pot = ADC(Pin(2), atten=ADC.ATTN_11DB)

led = PWM(Pin(8), freq=5000)

while True:
    new_val = pot.read_u16() / 2**6
    led.duty(int(new_val))
    sleep(0.1)
```

<!--
Sprachkonstrukte:
* mathematische Operatoren
* Casting, Datentypen
-->

---

## Wassersensor (1)

- funktioniert wie ein Potentiometer
* **TODO**: LED fünfmal schnell blinken lassen, wenn Wasser erkannt wird
* **Bonus**: Blinkfrequenz in Abhängigkeit von der Wassermenge
```py
# ...
def alarm_blink(led):
    for _ in range(10):
        led.value(not led.value())
        sleep(0.1)
# ...
```

<!--
Sprachkonstrukte:
* eigene Funktion
* for-Schleife

Hardware:
* Wassersensor
-->

---

## Wassersensor (2)

```py
# ...

WATER_THRES = 1000
        
water_sensor = ADC(Pin(1), atten=ADC.ATTN_11DB)
led = Pin(8, Pin.OUT)
led.value(1)

while True:
    water_value = water_sensor.read_u16()
    if water_value > WATER_THRES:
        print(f"Wasser erkannt: {water_value}")
        alarm(led)
        sleep(5)
    sleep(0.1)
```

<!--
Sprachkonstrukte:
* print mit f-string
* Konstante, Naming convention
-->

---

## Ultraschallsensor (1)

- Messung Abstand (2 cm .. 4 m) mit Schallimpuls und Laufzeitmessung
* Trigger-Pin als Ausgang: High-Impuls für 10 μs
* Echo-Pin als Eingang: Messung mit `machine.time_pulse_us()`

```py
class HCSR04:
    _SOUND_SPEED = 343.2
    def __init__(self, trigger_pin, echo_pin):
        self._trigger = Pin(trigger_pin, mode=Pin.OUT)
    def distance_mm(self):
        # ...
        return 42
```

* **TODO**: Implementierung Klasse und sekündliche Ausgabe des Abstands

<!--
Sprachkonstrukte:
* Klassen
* Zeitmessung

Hardware:
* Ultraschall
-->

---

## Ultraschallsensor (2)

```py
# ...
class HCSR04:
    _SOUND_SPEED = 0.34320 # mm/μs
    _MAX_RANGE = 4000 # mm

    def __init__(self, trigger_pin, echo_pin):
        self._trigger = machine.Pin(trigger_pin, machine.Pin.OUT)
        self._trigger.value(0)
        self._echo = machine.Pin(echo_pin, machine.Pin.IN)

    def distance_mm(self):
        self._trigger.value(0)
        time.sleep_us(5)

        self._trigger.value(1)
        time.sleep_us(10)
        self._trigger.value(0)

        timeout_us = int(2 * self._MAX_RANGE / self._SOUND_SPEED)
        pulse_time = machine.time_pulse_us(self._echo, 1, timeout_us)
        if pulse_time > 0:
            return pulse_time * self._SOUND_SPEED / 2
        return math.inf
```

<!--
_footer: ""
-->

---

## Ultraschallsensor (3)

```py
# ...
sensor = HCSR04(trigger_pin=5, echo_pin=6)

while True:
    distance = sensor.distance_mm()
    print(f"Abstand: {distance/10:.1f} cm")
    time.sleep(1)
```

---

# Digitale Sensoren und Aktoren

Temperatur, Luftfeuchtigkeit, Luftdruck, Display

<!--
header: MicroPython: Digitale Sensoren und Aktoren
-->

---

## Temperatur und Luftfeuchtigkeit (1)

- mit Sensor DHT-22
- Sensor kann nur im 2-Sekunden-Takt abgefragt werden

```py
import dht
# ...
# Daten-PIN mit Pull-Up
sensor = dht.DHT22(pin)
# ...
sensor.measure()
temp = sensor.temperature()
hum = sensor.humidity()
```

* **TODO**: lese Temperatur und Luftfeuchtigkeit in einer Funktion und gib beides "hübsch" aus
* Hinweis: Funktionen können (mehrere) Rückgabewerte haben

<!--
Hardware:
* DHT-22 und Familie
-->

---

## Temperatur und Luftfeuchtigkeit (2)

```py
# ...
def weather():
    sensor.measure()
    temp = sensor.temperature()
    hum = sensor.humidity()
    return temp, hum
while True:
    temp, hum = weather()
    print(f"Temperatur: {temp}° C\nLuftfeuchte: {hum} %")
    time.sleep(2)
```

<!--
Sprachkonstrukte:
* Funktion mit Rückgabewert
-->

---

## Temperatur, Luftdruck und Höhe (1)

- mit Sensor BMP-280
- basierend auf I2C

```py
import machine

i2c = machine.I2C(0)
i2c.scan()
i2c.readfrom(118, 240)
```

<!--
Sprachkonstrukte:
* externe Bibliothek

Hardware:
* I2C
* BMP280
-->

---

## Temperatur, Luftdruck und Höhe (2)

- Berechnung etwas komplex -> extra Bibliothek

```py
# ...
import bme280
sensor = bme280.BME280(i2c=i2c)

while True:
    print(f"Temperatur: {sensor.temperature}\nDruck: {sensor.pressure}")
    time.sleep(2)
```

* **TODO**: berechne die Höhe über dem Meer
* Hinweis 1: `sensor.read_pressure()` gibt den Druck in Pascal
* Hinweis 2: nutze die Barometrische Höhenformel bzw. Internationale Höhenformel

---

## Temperatur, Luftdruck und Höhe (3)

```py
# ...
def altitude(temp, pres):
    t = 273.15 + temp
    p0 = 1013.25
    return t/0.0065*(1-(pres/p0)**(1/5.255))

while True:
    t = sensor.read_temperature() / 100
    p = sensor.read_pressure() / 256 / 100
    alt = altitude(t, p)
    print(f"Temperatur: {t:.1f} °C\nDruck: {p:.1f} hPa\nHöhe: {alt:.1f} m")
    time.sleep(2)
```

---

## Display (1)

- mit Display SSD1306
- basierend auf I2C

#TODO

<!--
Sprachkonstrukte:
* Vererbung

Hardware:
* SPI
* SSD1306
-->

---

# Netzwerk und Kommunikation

WiFi, Bluetooth, API, Webserver

<!--
header: MicroPython: Netzwerk und Kommunikation
-->

---

## WiFi-Verbindung herstellen

```py
from time import sleep
import network

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
print(f"Connecting to network {WLAN_SSID!r}...")
wlan.connect(WLAN_SSID, WLAN_PSK)
while not wlan.isconnected():
    sleep(0.1)
print("network config:", wlan.ifconfig())
```

---

## Daten abrufen

```py
# ...
import requests
import json
# ...
headers = {
    'Accept': 'application/json',
}
r = requests.get(url, headers=headers)
if r.status_code == 200:
    data = r.json()
```

---

## Daten senden

```py
# ...
import requests
import json
# ...
headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer 1234',
}
data = {
    'hello': "World",
}
data_encoded = json.dumps(data).encode()
r = requests.post(url, data=data_encoded, headers=headers)
if r.status_code == 200:
    data = r.json()
```

---

# Projekt: Jetzt seid ihr am Zug!

Lasst eurer Kreativität freien Lauf!

<!--
header: MicroPython: Projekt: Jetzt seid ihr am Zug!
-->

---

## Aufgabe

#TODO

---

# The End

<!--
header: MicroPython
-->
