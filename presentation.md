---
marp: true
theme: default
class: invert
---

# Smart Home selbstgemacht
— Einstieg in die Programmierung mit MicroPython —

---

<!--
header: Workshop Micropython\n28.04.2024
paginate: true
-->

## Agenda

1. Unser Universum
1. Unsere Toolchain
1. Hello World
— Pause —
1. Sprachkonstrukte und Sensoren
1. Netzwerk
— Pause —
1. Projekt
1. Zusammenfassung

---

# Unser Universum

<!--
footer: Unser Universum
-->

---

<!--
* ESP32
* Python
* MicroPython
* Home Assistant
* Raspberry Pi
--->

![bg 70%](https://cdn.ttgtmedia.com/rms/onlineImages/iota-smart_home.jpg)
<!-- Quelle: https://www.computerweekly.com/de/definition/Smart-Home -->

---

# Toolchain

<!--
footer: Toolchain
-->

---

## Linkliste, Dokumentation, Präsentation

https://github.com/st31ny/micropython-workshop

---

## Werkzeuge

- Thonny: IDE für Python-Entwicklung mit MicroPython-Unterstützung
    - Download unter https://thonny.org
- ESP32-C3 SuperMini
    - dazu USB-Kabel, Sensoren, Breadboard
- 3er Gruppen mit einem Laptop und einem Bausatz

<!--
später: Messgerät, passende Sensoren, Lötkolben
-->

---

## Einrichtung

<!-- zeigen! -->
- Rechner per USB mit Chip verbinden
- Thonny starten
- Ersteinrichtung für MicroPython:
    - Extras > Optionen > Interpreter
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

# Hello World

<!--
footer: Hello World
-->

---

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

---

# Pause

---

# Sprachkonstrukte und Sensoren

<!--
footer: Sprachkonstrukte und Sensoren
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
-->

---

## Potentiometer und PWM (1)

<!--
interne Referenzspannung 1.1 V
-->
```py
from machine import Pin, ADC, PWM
from time import sleep

# ADC mit 11 dB Dämpfung auf Pin 2 => 150mV..2450mV
pot = ADC(Pin(2), atten=ADC.ATTN_11DB)
pot.read_u16() # gib Wert (0..65536)

# PWM mit 5 kHz auf Pin 8
led = PWM(Pin(8), freq=5000)
led.duty(512) # setze analogen Wert (0..1024)

# TODO: Dimme LED mit Poti.
```

<!--
Sprachkonstrukte:
* Kommentare
* benannte Parameter
-->

---

## Potentiometer und PWM (2)

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

# Netzwerk

<!--
footer: Netzwerk
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
r = requests.get(url, data=data_encoded, headers=headers)
if r.status_code == 200:
    data = r.json()
```

---

# Pause

---

# Projekt

<!--
footer: Projekt
-->

---

## Aufgabe

Ein Wassorsensor und eine Luftfeuchtesensor sollen überwacht werden. Wenn der Wassersensor Wasser detektiert oder die Luftfeuchtigkeit auf über 70 % steigt, soll ein App-Alarm ausgelöst werden.

---

# Zusammenfassung

<!--
footer: Zusammenfassung
-->

---

## Zusammenfassung

- flache Lernkurve
- Code schnell ausprobieren
- Vielzahl an Sensoren
- Integration in andere Systeme

---

# Vielen Dank

<!--
footer:
-->
