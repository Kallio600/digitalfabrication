from machine import ADC
from machine import Pin

from machine import Pin

#Relay connected to GP16
relay_pin = Pin(16, Pin.OUT)
relay_pin.off()  #valve off at start

#LED connected to GP17
led_pin = Pin(17, Pin.OUT)

def set_led(state: bool):
    led_pin.value(state)

led_pin.off()  #LED off

def start_irrigation():
    """Activate relay to open magnetic valve and turn on LED."""
    relay_pin.on()
    led_pin.on()

def stop_irrigation():
    """Deactivate relay to close magnetic valve and turn off LED."""
    relay_pin.off()
    led_pin.off()

def irrigation_test_auto(water_ok: bool):
    """Turn valve ON if water is present, otherwise OFF."""
    if water_ok:
        start_irrigation()
    else:
        stop_irrigation()



# Configure LED pin (active HIGH) - Red LED on the roof
led = Pin(15, Pin.OUT)

# Initialize ADCs
_temp_adc = ADC(4)    # Internal temperature sensor
_water_adc = ADC(26)  # GP26 (analog input for liquid level sensor)

_conversion_factor = 3.3 / 65535

def read_temperature():
    raw = _temp_adc.read_u16() * _conversion_factor
    return round(27 - (raw - 0.706) / 0.001721, 1)

def read_water_level():
    raw = _water_adc.read_u16()
    voltage = raw * _conversion_factor
    percent = (voltage / 3.3) * 100
    return max(0, min(100, round(percent)))

def water_present():
    raw = _water_adc.read_u16()
    is_present = raw > 50000

    # Control LED based on water status
    if is_present:
        led.off()  # water is OK
    else:
        led.on()   # water empty = turn on warning LED

    return is_present


