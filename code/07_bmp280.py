import machine
import time
# https://github.com/RuiSantosdotme/ESP-MicroPython/blob/master/code/WiFi/HTTP_Client_IFTTT_BME280/BME280.py
import bme280

i2c = machine.I2C(0)

# Scan nach allen Geräten
# i2c.scan()

sensor = bme280.BME280(i2c=i2c)

while True:
    print(f"Temperatur: {sensor.temperature}\nDruck: {sensor.pressure}")
    time.sleep(2)
