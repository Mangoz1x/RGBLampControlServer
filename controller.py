# controller.py

import time
import board
import neopixel
import threading
import random

# Configuration
LED_COUNT = 144  # Number of LEDs in your strip
PIN = board.D18  # GPIO pin for the data signal (18)
ORDER = neopixel.GRB  # Color order (WS2815 uses GRB)

# Initialize the LED strip object
pixels = neopixel.NeoPixel(PIN, LED_COUNT, brightness=0.2, auto_write=False, pixel_order=ORDER)

# Thread management
effect_thread = None
stop_event = threading.Event()

def set_brightness(brightness):
    """Set the brightness of the LED strip."""
    pixels.brightness = max(0.0, min(brightness, 1.0))  # Clamp between 0.0 and 1.0
    pixels.show()

def stop_current_effect():
    """Signal the current effect to stop."""
    global stop_event, effect_thread
    if effect_thread and effect_thread.is_alive():
        stop_event.set()
        effect_thread.join()

def start_effect(effect_func, *args, **kwargs):
    """Start a new lighting effect in a separate thread."""
    global effect_thread, stop_event
    stop_current_effect()
    stop_event.clear()
    effect_thread = threading.Thread(target=effect_func, args=args, kwargs=kwargs)
    effect_thread.start()

def color_fill(color):
    """Fill the strip with a single color."""
    stop_event.clear()
    pixels.fill(color)
    pixels.show()

def rainbow_cycle(wait=0.01):
    """Display a rainbow across the LEDs."""
    try:
        while not stop_event.is_set():
            for j in range(255):
                if stop_event.is_set():
                    break
                for i in range(LED_COUNT):
                    rc_index = (i * 256 // LED_COUNT) + j
                    pixels[i] = wheel(rc_index & 255)
                pixels.show()
                time.sleep(wait)
    except KeyboardInterrupt:
        pass

def breathing_effect(color, steps=50, wait=0.05):
    """Create a breathing effect by gradually adjusting brightness."""
    try:
        while not stop_event.is_set():
            for step in range(steps):
                if stop_event.is_set():
                    break
                brightness = step / steps
                scaled_color = tuple(int(c * brightness) for c in color)
                pixels.fill(scaled_color)
                pixels.show()
                time.sleep(wait)
            for step in range(steps, 0, -1):
                if stop_event.is_set():
                    break
                brightness = step / steps
                scaled_color = tuple(int(c * brightness) for c in color)
                pixels.fill(scaled_color)
                pixels.show()
                time.sleep(wait)
    except KeyboardInterrupt:
        pass

def theater_chase(color, alternate_color, wait=0.1):
    """Create a theater chase effect."""
    try:
        while not stop_event.is_set():
            for offset in range(3):
                if stop_event.is_set():
                    break
                for i in range(LED_COUNT):
                    if (i + offset) % 3 == 0:
                        pixels[i] = color
                    else:
                        pixels[i] = alternate_color
                pixels.show()
                time.sleep(wait)
    except KeyboardInterrupt:
        pass

def sparkle_effect(color, alternate_color, count=20, wait=0.05, fade_steps=10):
    """Create a sparkle effect with fading."""
    try:
        while not stop_event.is_set():
            # Fill the LEDs with the alternate color
            pixels.fill(alternate_color)
            pixels.show()

            # Perform the sparkle effect with the primary color
            for _ in range(count):
                if stop_event.is_set():
                    break
                pixel_index = random.randint(0, LED_COUNT - 1)

                # Set the initial sparkle color
                pixels[pixel_index] = color
                pixels.show()
                time.sleep(wait)

                # Gradually fade back to the alternate color
                for step in range(fade_steps):
                    if stop_event.is_set():
                        break
                    brightness = 1 - (step / fade_steps)
                    faded_color = tuple(
                        int(c * brightness + a * (1 - brightness))
                        for c, a in zip(color, alternate_color)
                    )
                    pixels[pixel_index] = faded_color
                    pixels.show()
                    time.sleep(wait / fade_steps)

                # Ensure it ends at the alternate color
                pixels[pixel_index] = alternate_color
                pixels.show()
    except KeyboardInterrupt:
        pass

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

def cleanup():
    """Turn off all LEDs."""
    pixels.fill((0, 0, 0))
    pixels.show()
