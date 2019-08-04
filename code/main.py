from machine import SPI, Pin
import tinypico as TinyPICO
from micropython_dotstar import DotStar

# Configure SPI for controlling the DotStar
# Internally we are using software SPI for this as the pins being used are not hardware SPI pins
spi = SPI(sck=Pin( TinyPICO.DOTSTAR_CLK ), mosi=Pin( TinyPICO.DOTSTAR_DATA ), miso=Pin( TinyPICO.SPI_MISO) )
# Create a DotStar instance
dotstar = DotStar(spi, 1, brightness = 0.5 ) # Just one DotStar, half brightness
# Turn on the power to the DotStar
TinyPICO.set_dotstar_power(True)

# Read the data every 15 seconds
update_interval = 5
# Make sure it fires immediately by starting it in the past
update_temp_time = time.time() - 10

def print_temp():
    global update_interval
    global update_temp_time

    # We only run the contents of this function every 5 seconds
    if update_temp_time < time.time():
        update_temp_time = time.time() + update_interval

        # Grab the temperates and print them
        print("\nInternal PICO-D4 Temp: {:.2f}°C".format( TinyPICO.get_internal_temp_C() ) )
        print("Battery Voltage is {}V".format( TinyPICO.get_battery_voltage() ) )
        print("Battery Charge State is {}\n".format( TinyPICO.get_battery_charging() ) )

def do_things():
# Create a colour wheel index int
    color_index = 0

    # Rainbow colours on the Dotstar
    while True:
        # Get the R,G,B values of the next colour
        r,g,b = TinyPICO.dotstar_color_wheel( color_index )
        # Set the colour on the dotstar
        dotstar[0] = ( r, g, b, 0.5)
        # Increase the wheel index
        color_index += 1
        # Sleep for 20ms so the colour cycle isn't too fast
        time.sleep_ms(20)

        # Print the internal PICO-D4 temperature in C
        print_temp()

        # Connect / Maintain internet connection.
        do_connect(config)
        time.sleep_us(100)

import _thread
import time
_thread.start_new_thread(do_things, ())

gc.collect()
