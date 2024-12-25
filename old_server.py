from flask import Flask, request, jsonify
from flask_cors import CORS
import controller
import threading

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def index():
    return "WS2815 RGB Strip Control API"

@app.route('/color_fill', methods=['POST'])
def api_color_fill():
    data = request.get_json()
    color = data.get('color')
    if not color or len(color) != 3:
        return jsonify({"error": "Invalid color. Provide a list of three integers [R, G, B]."}), 400
    try:
        color = tuple(int(c) for c in color)
    except ValueError:
        return jsonify({"error": "Color values must be integers."}), 400
    controller.start_effect(controller.color_fill, color)
    return jsonify({"status": "Color fill effect started.", "color": color}), 200

@app.route('/rainbow_cycle', methods=['POST'])
def api_rainbow_cycle():
    data = request.get_json()
    colors = data.get('colors')
    wait = data.get('wait', 0.05)
    gradient_steps = data.get('gradient_steps', 20)
    
    # Validate colors
    if not colors or not isinstance(colors, list) or not all(isinstance(color, list) and len(color) == 3 for color in colors):
        return jsonify({"error": "Invalid colors. Provide a list of RGB lists, e.g., [[R, G, B], ...]."}), 400
    
    try:
        # Convert colors to tuples of integers
        colors = [tuple(int(c) for c in color) for color in colors]
        wait = float(wait)
    except ValueError:
        return jsonify({"error": "Colors must be integers and wait must be a float."}), 400
    
    controller.start_effect(controller.rainbow_cycle, colors, wait, gradient_steps)
    return jsonify({
        "status": "Rainbow cycle effect started.",
        "colors": colors,
        "wait": wait
    }), 200

@app.route('/breathing_effect', methods=['POST'])
def api_breathing_effect():
    data = request.get_json()
    color = data.get('color')
    steps = data.get('steps', 50)
    wait = data.get('wait', 0.05)
    if not color or len(color) != 3:
        return jsonify({"error": "Invalid color. Provide a list of three integers [R, G, B]."}), 400
    try:
        color = tuple(int(c) for c in color)
        steps = int(steps)
        wait = float(wait)
    except ValueError:
        return jsonify({"error": "Invalid parameters. Ensure color is integers and steps is int, wait is float."}), 400
    controller.start_effect(controller.breathing_effect, color, steps, wait)
    return jsonify({"status": "Breathing effect started.", "color": color, "steps": steps, "wait": wait}), 200

@app.route('/theater_chase', methods=['POST'])
def api_theater_chase():
    data = request.get_json()
    color = data.get('color')
    alternate_color = data.get('alternate_color')
    wait = data.get('wait', 0.1)
    if not color or len(color) != 3 or not alternate_color or len(alternate_color) != 3:
        return jsonify({"error": "Invalid colors. Provide lists of three integers for 'color' and 'alternate_color'."}), 400
    try:
        color = tuple(int(c) for c in color)
        alternate_color = tuple(int(c) for c in alternate_color)
        wait = float(wait)
    except ValueError:
        return jsonify({"error": "Color values must be integers and wait must be a float."}), 400
    controller.start_effect(controller.theater_chase, color, alternate_color, wait)
    return jsonify({"status": "Theater chase effect started.", "color": color, "alternate_color": alternate_color, "wait": wait}), 200

@app.route('/sparkle_effect', methods=['POST'])
def api_sparkle_effect():
    data = request.get_json()
    color = data.get('color')
    alternate_color = data.get('alternate_color')
    count = data.get('count', 20)
    wait = data.get('wait', 0.05)
    fade_steps = data.get('fade_steps', 10)
    if not color or len(color) != 3 or not alternate_color or len(alternate_color) != 3:
        return jsonify({"error": "Invalid colors. Provide lists of three integers for 'color' and 'alternate_color'."}), 400
    try:
        color = tuple(int(c) for c in color)
        alternate_color = tuple(int(c) for c in alternate_color)
        count = int(count)
        wait = float(wait)
        fade_steps = int(fade_steps)
    except ValueError:
        return jsonify({"error": "Invalid parameters. Ensure colors are integers and count, fade_steps are integers, wait is float."}), 400
    controller.start_effect(controller.sparkle_effect, color, alternate_color, count, wait, fade_steps)
    return jsonify({
        "status": "Sparkle effect started.",
        "color": color,
        "alternate_color": alternate_color,
        "count": count,
        "wait": wait,
        "fade_steps": fade_steps
    }), 200

@app.route('/set_brightness', methods=['POST'])
def api_set_brightness():
    data = request.get_json()
    brightness = data.get('brightness')
    if brightness is None:
        return jsonify({"error": "Brightness value is required."}), 400
    try:
        brightness = float(brightness)
        if not (0.0 <= brightness <= 1.0):
            raise ValueError
    except ValueError:
        return jsonify({"error": "Brightness must be a float between 0.0 and 1.0."}), 400
    controller.set_brightness(brightness)
    return jsonify({"status": "Brightness updated.", "brightness": brightness}), 200

@app.route('/stop', methods=['POST'])
def api_stop():
    controller.stop_current_effect()
    controller.cleanup()
    return jsonify({"status": "All effects stopped and LEDs turned off."}), 200

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        controller.cleanup()