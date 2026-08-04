from machine import Pin, I2C
import ssd1306
import gfx
from time import sleep

i2c = I2C(0)

# Breite und Höhe des Displays in Pixeln
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
graphics = gfx.GFX(oled_width, oled_height, oled.pixel)

while True:
    oled.fill(0) # Bildschirm löschen

    # Bereite den Text vor
    oled.text("Hallo Welt!", 0, 0)
    oled.text("Micropython", 0, 16)
    oled.text("Workshop", 0, 32)
    oled.text("2026", 0, 48)

    # Schreibe den Text auf das Display
    oled.show()

    invert = True
    for _ in range(5):
        sleep(1)
        oled.invert(invert) # invertiere Display
        invert = not invert
        oled.show()

    oled.fill(0)
    oled.invert(False)
    oled.show()

    graphics.line(0, 0, 127, 20, 1) # Linie
    graphics.rect(10, 10, 50, 30, 1) # Rechteck (oder fill_rect())
    graphics.fill_circle(64, 32, 10, 1) # Kreis (oder circle())
    graphics.fill_triangle(84,32,90,45,100,40,1) # Dreieck (oder triangle())
    oled.show()

    sleep(4)

    # Kreis von links nach rechts wandern lassen
    for i in range(0, oled_width+10, 4):
        oled.fill(0)
        graphics.fill_circle(i, 32, 10, 1)
        oled.show()

    # Text von links nach rechts wandern lassen
    for i in range(0, 2*(oled_width+1), 1):
        oled.fill(0)
        oled.text("Hallo Welt!", -oled_width+i, 32)
        oled.show()
