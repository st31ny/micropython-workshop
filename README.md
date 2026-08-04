Programmierung von Embedded Systems mit MicroPython
===================================================

Seit einigen Jahren gibt es diverse Smart-Home-Geräte am Markt, die sich leider allzu oft als Sicherheitslücke, Datenschleuder oder — nach der Pleite der Firmen — teure Briefbeschwerer herausstellen. Grund genug, die Sache selbst in die Hand zu nehmen!

Dank der Sprache MicroPython ist die Programmierung von Mikrocontrollern so einfach wie nie zuvor. In diesem Workshop werden wir erste Schritte mit MicroPython auf dem verbreiteten ESP32-Chip wagen und kleine nützliche Projekte zur Automatisierung der eigenen vier Wände realisieren (z. B. einen Wassersensor, ein Thermometer und ein Display).

Links
-----

* [Präsentation zum Workshop](https://st31ny.github.io/micropython-workshop)
* [ESP32-Modellübersicht](https://www.espressif.com/en/products/socs)
* [Datenblatt ESP32 Mini](https://www.espressif.com/sites/default/files/documentation/esp32-c3-mini-1_datasheet_en.pdf)
* [Pinout](https://www.nologo.tech/assets/img/esp32/esp32c3supermini/esp32c3foot1.png)
    * in Software: GPIO-Nummern
    * LED: GPIO 8
    * BOOT-Button: GPIO 9
* [Firmware](https://www.micropython.org/download/ESP32_GENERIC_C3/)
* [Dokumentation MicroPython](https://docs.micropython.org/en/latest/esp32/quickref.html)
* [Dokumentation Python](https://docs.python.org/3/)
* [Thonny-IDE](https://thonny.org/)
* [esptool](https://docs.espressif.com/projects/esptool/en/latest/esp32/)
* Hardware
    * [ESP32-C3 SuperMini](https://www.ebay.de/itm/157669215579)
    * [Elektronik-Bastelkiste ELEGOO Upgraded Elektronics Fun Kit](https://www.amazon.de/-/dp/B01M7N4WB6)
        * [LED-Vorwiderstandsrechner](https://www.elektronik-kompendium.de/sites/bau/1109111.htm)
        * [Widerstandsfarbcode](https://www.elektronik-kompendium.de/sites/bau/1109051.htm)
    * [Wassersensor](https://www.ebay.de/itm/376829936950)
    * [Display SSD1306 I2C/IIC](https://www.ebay.de/itm/177392745668)
        * [Bibliothek für das SSD1306](https://github.com/adafruit/micropython-adafruit-ssd1306/blob/master/ssd1306.py)
        * [Bibliothek für Grafik](https://github.com/adafruit/micropython-adafruit-gfx/blob/master/gfx.py)
    * [Ultraschall HC-SR04](https://www.ebay.de/itm/185904806389)
    * [Radar RCWL-0516](https://www.ebay.de/itm/153308558247)
    * [Temperatur/Feuchtigkeit DHT-22](https://www.ebay.de/itm/317454484565)
    * [Temperatur/Druck BMP280](https://www.ebay.de/itm/317569138885)
        * [Bibliothek für den BMP280](https://github.com/RuiSantosdotme/ESP-MicroPython/blob/master/code/WiFi/HTTP_Client_IFTTT_BME280/BME280.py)
* Tutorials
    * [Getting started](https://randomnerdtutorials.com/getting-started-thonny-micropython-python-ide-esp32-esp8266/)
    * [MicroPython/Python basics](https://randomnerdtutorials.com/micropython-programming-basics-esp32-esp8266/)
    * [GPIO](https://randomnerdtutorials.com/micropython-gpios-esp32-esp8266/)
    * [DHT-22](https://randomnerdtutorials.com/esp32-esp8266-dht11-dht22-micropython-temperature-humidity-sensor/)
    * [BME280](https://randomnerdtutorials.com/micropython-sensor-readings-email-esp32-esp826/)
    * [RCWL-0516](https://randomnerdtutorials.com/micropython-rcwl-0516-esp32-esp8266/)
    * [HC-SR04](https://randomnerdtutorials.com/micropython-hc-sr04-ultrasonic-esp32-esp8266/)
    * [SSD1306](https://randomnerdtutorials.com/micropython-ssd1306-oled-scroll-shapes-esp32-esp8266/)

Firmwareinstallation
--------------------

Bevor MicroPython genutzt werden kann, muss es auf dem Chip installiert werden. Dieser Vorgang wird als "Flashen" bezeichnet und kann entweder mit dem esptool oder mit Thonny gemacht werden. Dafür wird eine zum Chip passende Firmwaredatei für MicroPython benötigt.

* per esptool
```
esptool --chip esp32c3 --port /dev/ttyACM0 erase_flash
esptool --chip esp32c3 --port /dev/ttyACM0 --baud 460800 write_flash -z 0x0 ESP32_GENERIC_C3-xxx.bin
```
* per Thonny:
    * unter Werkzeuge > Optionen > Interpreter
    * Auswahl Interpreter: "MicroPython (ESP32)"
    * "MicroPython installieren oder aktualisieren"

Einrichtung Thonny IDE/Firmwareinstallation
-------------------------------------------

* öffne Werkzeuge > Optionen > Interpreter
* Auswahl Interpreter: "MicroPython (ESP32)"
* Auswahl Port
* "OK"
* in der "Kommondozeile": `help()`
    * Hier sollte eine lange Hilfe kommen, die mit "Welcome to MicroPython on the ESP32!" beginnt.

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
