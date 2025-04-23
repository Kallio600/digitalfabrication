from functions import read_temperature, water_present, start_irrigation, stop_irrigation, set_led
from ui import display_status
import time

irrigating = False
led_state = False
irrigation_start_time = 0
last_irrigation_time = 0  # Time of last irrigation, irrigation starts only onece per 24h
IRRIGATION_DURATION =  18000 # 15h = 18000sec
TEMP_THRESHOLD = 15
IRRIGATION_COOLDOWN = 86400  # 24h = 86400 sec

while True:
    temp = read_temperature()
    water_ok = water_present()
    current_time = time.time()

    time_since_last = current_time - last_irrigation_time

    # Start irrigation only if all conditions are met
    if (
        temp >= TEMP_THRESHOLD and
        water_ok and
        not irrigating and
        time_since_last >= IRRIGATION_COOLDOWN
    ):
        start_irrigation()
        irrigation_start_time = current_time
        last_irrigation_time = current_time  # mark last time
        irrigating = True

    # Stop if time runs out or water runs out
    if irrigating:
        if (current_time - irrigation_start_time >= IRRIGATION_DURATION) or not water_ok:
            stop_irrigation()
            irrigating = False

    # LED and display logic
    if irrigating:
        led_state = not led_state
        set_led(led_state)
        display_status(temp, water_ok, irrigating=True, flash_irrigating=led_state)
    else:
        set_led(False)
        display_status(temp, water_ok, irrigating=False)

    time.sleep(1)
