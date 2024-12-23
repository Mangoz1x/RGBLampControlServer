import time
import board
import neopixel

# Configuration
LED_COUNT = 144  # Number of LEDs in your strip
PIN = board.D18  # GPIO pin for the data signal (18)
ORDER = neopixel.GRB  # Color order (WS2815 uses GRB)

# Create the LED strip object
pixels = neopixel.NeoPixel(PIN, LED_COUNT, brightness=0.2, auto_write=False, pixel_order=ORDER)

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

def breathing_effect(color, steps=50, wait=0.05):
    """Create a breathing effect by gradually adjusting brightness."""
    for step in range(steps):
        brightness = step / steps
        scaled_color = tuple(int(c * brightness) for c in color)
        pixels.fill(scaled_color)
        pixels.show()
        time.sleep(wait)
    for step in range(steps, 0, -1):
        brightness = step / steps
        scaled_color = tuple(int(c * brightness) for c in color)
        pixels.fill(scaled_color)
        pixels.show()
        time.sleep(wait)

def theater_chase(color, alternate_color, wait):
    """Create a theater chase effect."""
    for step in range(10):  # Number of cycles
        for offset in range(3):
            for i in range(LED_COUNT):
                if (i + offset) % 3 == 0:
                    pixels[i] = color
                else:
                    pixels[i] = alternate_color
            pixels.show()
            time.sleep(wait)

def sparkle_effect(color, alternate_color, count=20, wait=0.05, fade_steps=10):
    """Randomly sparkle LEDs with a fading effect."""
    import random

    for _ in range(count):
        pixel_index = random.randint(0, LED_COUNT - 1)

        # Set the initial sparkle color
        pixels[pixel_index] = color
        pixels.show()
        time.sleep(wait)

        # Gradually fade to the alternate color
        for step in range(fade_steps):
            brightness = 1 - (step / fade_steps)
            faded_color = tuple(int(c * brightness) for c in color)
            pixels[pixel_index] = faded_color
            pixels.show()
            time.sleep(wait / fade_steps)

        # Ensure it ends at the alternate color
        pixels[pixel_index] = alternate_color
        pixels.show()

try:
    while True:
        color_fill((255, 100, 50))  # White
        time.sleep(1)
        rainbow_cycle(0.01)  # Rainbow
        breathing_effect((0, 0, 255))  # Blue breathing
        theater_chase((255, 0, 0), (0,255,0), 0.1)  # Red theater chase
        sparkle_effect((0, 255, 0), (0, 0, 0))  # Green sparkles
except KeyboardInterrupt:
    pixels.fill((0, 0, 0))
    pixels.show()
