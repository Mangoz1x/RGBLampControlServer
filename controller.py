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
    print(f"Brightness set to {pixels.brightness}")

def stop_current_effect():
    """Signal the current effect to stop."""
    global stop_event, effect_thread
    if effect_thread and effect_thread.is_alive():
        stop_event.set()
        effect_thread.join()
        print("Current effect stopped.")

def start_effect(effect_func, *args, **kwargs):
    """Start a new lighting effect in a separate thread."""
    global effect_thread, stop_event
    stop_current_effect()
    stop_event.clear()
    effect_thread = threading.Thread(target=effect_func, args=args, kwargs=kwargs)
    effect_thread.start()
    print(f"Effect {effect_func.__name__} started with args: {args}, kwargs: {kwargs}")

def interpolate(color1, color2, factor):
    """
    Interpolate between two colors.

    Args:
        color1 (tuple): RGB color tuple.
        color2 (tuple): RGB color tuple.
        factor (float): Interpolation factor between 0.0 and 1.0.

    Returns:
        tuple: Interpolated RGB color.
    """
    return tuple(int(c1 + (c2 - c1) * factor) for c1, c2 in zip(color1, color2))

def color_fill(color):
    """Fill the strip with a single color."""
    stop_event.clear()
    pixels.fill(color)
    pixels.show()
    print(f"Color fill with {color}")

def rainbow_cycle(colors, wait=0.05):
    """
    Cycle through a list of colors with smooth gradients, moving left.

    Args:
        colors (list of tuples): List of RGB color tuples.
        wait (float): Time to wait between cycles in seconds.
    """
    try:
        print(f"Starting rainbow_cycle with colors: {colors}, wait: {wait}")
        num_colors = len(colors)
        if num_colors < 2:
            print("At least two colors are required for a gradient.")
            return

        # Define the number of gradient steps between each pair of colors
        gradient_steps_per_transition = LED_COUNT // (num_colors * 2) # Adjust for smoother or coarser gradients

        # Total number of steps in the entire cycle
        total_steps = num_colors * gradient_steps_per_transition

        # Initialize step offset
        step = 0

        while not stop_event.is_set():
            for i in range(LED_COUNT):
                # Calculate the position in the gradient
                pos = (i + step) % total_steps

                # Determine which transition this position is in
                transition_index = pos // gradient_steps_per_transition
                # Find the two colors to interpolate between
                color1 = colors[transition_index % num_colors]
                color2 = colors[(transition_index + 1) % num_colors]
                # Determine the interpolation factor
                factor = (pos % gradient_steps_per_transition) / gradient_steps_per_transition
                # Interpolate the color
                color = interpolate(color1, color2, factor)

                # Assign the color to the pixel
                pixels[i] = color

            # Update the LEDs
            pixels.show()

            # Increment step to move the gradient
            step = (step + 1) % total_steps

            # Wait before the next update
            time.sleep(wait)
    except Exception as e:
        print(f"Error in rainbow_cycle: {e}")

def breathing_effect(color, steps=50, wait=0.05):
    """Create a breathing effect by gradually adjusting brightness."""
    try:
        while not stop_event.is_set():
            for step_val in range(steps):
                if stop_event.is_set():
                    break
                brightness = step_val / steps
                scaled_color = tuple(int(c * brightness) for c in color)
                pixels.fill(scaled_color)
                pixels.show()
                time.sleep(wait)
            for step_val in range(steps, 0, -1):
                if stop_event.is_set():
                    break
                brightness = step_val / steps
                scaled_color = tuple(int(c * brightness) for c in color)
                pixels.fill(scaled_color)
                pixels.show()
                time.sleep(wait)
    except Exception as e:
        print(f"Error in breathing_effect: {e}")

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
    except Exception as e:
        print(f"Error in theater_chase: {e}")

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
                for step_val in range(fade_steps):
                    if stop_event.is_set():
                        break
                    brightness = 1 - (step_val / fade_steps)
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
    except Exception as e:
        print(f"Error in sparkle_effect: {e}")

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
    print("Cleanup: All LEDs turned off.")
