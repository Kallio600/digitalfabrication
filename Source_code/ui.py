from oled import OLED_1inch3

oled = OLED_1inch3()

def display_status(temp, water_ok, irrigating=False, flash_irrigating=False):
    oled.fill(0)
    oled.text("{:.1f} C".format(temp), 5, 15, oled.white)

    if irrigating:
        if flash_irrigating:
            oled.text("Irrigating...", 10, 44, oled.white)
    else:
        if water_ok:
            oled.text("Water OK", 10, 44, oled.white)
        else:
            oled.text("Fill tank!", 10, 44, oled.white)

    oled.rect(0, 0, 128, 64, oled.white)
    oled.show()
