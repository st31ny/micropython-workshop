import machine
import time
# https://github.com/RuiSantosdotme/ESP-MicroPython/blob/master/code/WiFi/HTTP_Client_IFTTT_BME280/BME280.py
import bme280

i2c = machine.I2C(0)

# Scan nach allen Geräten
# i2c.scan()

sensor = bme280.BME280(i2c=i2c)

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
