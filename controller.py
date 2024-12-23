import time
import board
import neopixel

# Configuration
LED_COUNT = 144  # Number of LEDs in your strip
PIN = board.D18  # GPIO pin for the data signal (18)
ORDER = neopixel.GRB  # Color order (WS2815 uses GRB)

# Create the LED strip object
pixels = neopixel.NeoPixel(PIN, LED_COUNT, brightness=0.5, auto_write=False, pixel_order=ORDER)

def color_fill(color):
    """Wipe color across the strip one LED at a time."""
    for i in range(LED_COUNT):
        pixels[i] = color
        pixels.show()

def rainbow_cycle(wait):
    """Display a rainbow across the LEDs."""
    for j in range(255):
        for i in range(LED_COUNT):
            rc_index = (i * 256 // LED_COUNT) + j
            pixels[i] = wheel(rc_index & 255)
        pixels.show()
        time.sleep(wait)

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    else:
        pos -= 170
        return (pos * 3, 0, 255 - pos * 3)

try:
    while True:
        color_fill((255, 100, 50))  # White
        time.sleep(1)
        rainbow_cycle(0.01)  # Rainbow
except KeyboardInterrupt:
    pixels.fill((0, 0, 0))
    pixels.show()