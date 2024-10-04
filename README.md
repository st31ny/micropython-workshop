Einstieg in die Programmierung von Microcontrollern mit MicroPython
===================================================================

Seit einigen Jahren gibt es diverse Smart-Home-Geräte am Markt, die sich leider allzu oft als Sicherheitslücke, Datenschleuder oder — nach der Pleite der Firmen — teure Briefbeschwerer herausstellen. Grund genug, die Sache selbst in die Hand zu nehmen!

Dank der Sprache MicroPython ist die Programmierung von Mikrocontrollern so einfach wie nie zuvor. In diesem Workshop werden wir erste Schritte mit MicroPython auf dem verbreiteten ESP32-Chip wagen und kleine nützliche Projekte zur Automatisierung der eigenen vier Wände realisieren (z. B. einen Wassersensor und ein Thermometer).

Links
-----

* [Präsentation zum Workshop](https://st31ny.github.io/micropython-workshop)
* [ESP32-C3 SuperMini eBay](https://www.ebay.de/itm/285630123712)
* [ESP32-Modellübersicht](https://www.espressif.com/en/products/socs)
* [Datenblatt ESP32 Mini](https://www.espressif.com/sites/default/files/documentation/esp32-c3-mini-1_datasheet_en.pdf)
* [Pinout](https://www.nologo.tech/assets/img/esp32/esp32c3supermini/esp32c3foot1.png)
    * in Software: GPIO-Nummern
* [Firmware](https://www.micropython.org/download/ESP32_GENERIC_C3/)
* [Dokumentation MicroPython](https://docs.micropython.org/en/latest/esp32/quickref.html)
* [Thonny-IDE](https://thonny.org/)
* [esptool](https://docs.espressif.com/projects/esptool/en/latest/esp32/)
* Tutorials
    * [Getting started](https://randomnerdtutorials.com/getting-started-thonny-micropython-python-ide-esp32-esp8266/)
    * [MicroPython/Python basics](https://randomnerdtutorials.com/micropython-programming-basics-esp32-esp8266/)
    * [GPIO](https://randomnerdtutorials.com/micropython-gpios-esp32-esp8266/)

Firmwareinstallation
--------------------

Bevor MicroPython genutzt werden kann, muss es auf dem Chip installiert werden. Dieser Vorgang wird als "Flashen" bezeichnet und kann entweder mit dem esptool oder mit Thonny gemacht werden. Dafür wird eine zum Chip passende Firmwaredatei für MicroPython benötigt.

* per esptool
```
esptool --chip esp32c3 --port /dev/ttyACM0 erase_flash
esptool --chip esp32c3 --port /dev/ttyACM0 --baud 460800 write_flash -z 0x0 ESP32_GENERIC_C3-20240222-v1.22.2.bin
```
* per Thonny:
    * unter Extras > Optionen > Interpreter
    * Auswahl Interpreter: "MicroPython (ESP32)"
    * "MicroPython installieren oder aktualisieren"

Einrichtung Thonny IDE/Firmwareinstallation
-------------------------------------------

* öffne Extras > Optionen > Interpreter
* Auswahl Interpreter: "MicroPython (ESP32)"
* Auswahl Port
* "OK"

* in der "Kommondozeile": `help()`

Hello World mit LED
-------------------

Interaktiv:
```py
import machine
pin8 = machine.Pin(8, machine.Pin.OUT)
pin8.value(0)
pin8.value(1)
```

per Skript auf Gerät:
* "Speichern" > Micropython device > "main.py"
* Code:
```py
from machine import Pin
from time import sleep
led = Pin(8, Pin.OUT)
while True:
    led.value(not led.value())
    sleep(1)
```
* Start per RST-Button (oder Strg+D)
* zum Beenden: 🛑 (Strg+F2)

Codebeispiele
-------------

Siehe Ordner `code` für kommentierte Codeschnipsel für bestimmte Sensoren.

Pin-Out
-------

![](https://www.nologo.tech/assets/img/esp32/esp32c3supermini/esp32c3foot1.png)
