# server.py

from flask import Flask, request, jsonify
from flask_cors import CORS
import threading
from db import load_database, save_database, update_database, remove_from_database, get_from_database

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

DATABASE_FILE = 'database.json'
DATABASE_LOCK = threading.Lock()

@app.route('/')
def index():
    return "WS2815 RGB Strip Control API with Database"

# Existing APIs updated to write to the database only
def extract_api_parameters(data, required_fields, optional_fields=None):
    """
    Utility function to extract and validate parameters from request data.

    :param data: The JSON data from the request.
    :param required_fields: A list of required fields.
    :param optional_fields: A dict of optional fields with default values.
    :return: Tuple of (extracted_params, error_message)
    """
    if optional_fields is None:
        optional_fields = {}
    params = {}
    # Check required fields
    for field in required_fields:
        if field not in data:
            return None, f"Missing required field: {field}"
        params[field] = data[field]
    # Handle optional fields
    for field, default in optional_fields.items():
        params[field] = data.get(field, default)
    return params, None

@app.route('/color_fill', methods=['POST'])
def api_color_fill():
    data = request.get_json()
    params, error = extract_api_parameters(data, ['color'])
    if error:
        return jsonify({"error": error}), 400
    color = params['color']
    if not isinstance(color, list) or len(color) != 3:
        return jsonify({"error": "Invalid color. Provide a list of three integers [R, G, B]."}), 400
    try:
        color = [int(c) for c in color]
    except ValueError:
        return jsonify({"error": "Color values must be integers."}), 400
    update_database('color_fill', {"color": color})
    return jsonify({"status": "Color fill parameters saved.", "color": color}), 200

@app.route('/rainbow_cycle', methods=['POST'])
def api_rainbow_cycle():
    data = request.get_json()
    required = ['colors']
    optional = {'wait': 0.05, 'gradient_steps': 20}
    params, error = extract_api_parameters(data, required, optional)
    if error:
        return jsonify({"error": error}), 400
    colors = params['colors']
    wait = params['wait']
    gradient_steps = params['gradient_steps']
    # Validate colors
    if not isinstance(colors, list) or not all(isinstance(color, list) and len(color) == 3 for color in colors):
        return jsonify({"error": "Invalid colors. Provide a list of RGB lists, e.g., [[R, G, B], ...]."}), 400
    try:
        colors = [[int(c) for c in color] for color in colors]
        wait = float(wait)
        gradient_steps = int(gradient_steps)
    except ValueError:
        return jsonify({"error": "Colors must be integers, wait must be a float, and gradient_steps must be an integer."}), 400
    update_database('rainbow_cycle', {
        "colors": colors,
        "wait": wait,
        "gradient_steps": gradient_steps
    })
    return jsonify({
        "status": "Rainbow cycle parameters saved.",
        "colors": colors,
        "wait": wait,
        "gradient_steps": gradient_steps
    }), 200

@app.route('/breathing_effect', methods=['POST'])
def api_breathing_effect():
    data = request.get_json()
    required = ['color']
    optional = {'steps': 50, 'wait': 0.05}
    params, error = extract_api_parameters(data, required, optional)
    if error:
        return jsonify({"error": error}), 400
    color = params['color']
    steps = params['steps']
    wait = params['wait']
    if not isinstance(color, list) or len(color) != 3:
        return jsonify({"error": "Invalid color. Provide a list of three integers [R, G, B]."}), 400
    try:
        color = [int(c) for c in color]
        steps = int(steps)
        wait = float(wait)
    except ValueError:
        return jsonify({"error": "Invalid parameters. Ensure color is integers, steps is int, wait is float."}), 400
    update_database('breathing_effect', {
        "color": color,
        "steps": steps,
        "wait": wait
    })
    return jsonify({"status": "Breathing effect parameters saved.", "color": color, "steps": steps, "wait": wait}), 200

@app.route('/theater_chase', methods=['POST'])
def api_theater_chase():
    data = request.get_json()
    required = ['color', 'alternate_color']
    optional = {'wait': 0.1}
    params, error = extract_api_parameters(data, required, optional)
    if error:
        return jsonify({"error": error}), 400
    color = params['color']
    alternate_color = params['alternate_color']
    wait = params['wait']
    if not isinstance(color, list) or len(color) != 3 or not isinstance(alternate_color, list) or len(alternate_color) != 3:
        return jsonify({"error": "Invalid colors. Provide lists of three integers for 'color' and 'alternate_color'."}), 400
    try:
        color = [int(c) for c in color]
        alternate_color = [int(c) for c in alternate_color]
        wait = float(wait)
    except ValueError:
        return jsonify({"error": "Color values must be integers and wait must be a float."}), 400
    update_database('theater_chase', {
        "color": color,
        "alternate_color": alternate_color,
        "wait": wait
    })
    return jsonify({
        "status": "Theater chase parameters saved.",
        "color": color,
        "alternate_color": alternate_color,
        "wait": wait
    }), 200

@app.route('/sparkle_effect', methods=['POST'])
def api_sparkle_effect():
    data = request.get_json()
    required = ['color', 'alternate_color']
    optional = {'count': 20, 'wait': 0.05, 'fade_steps': 10}
    params, error = extract_api_parameters(data, required, optional)
    if error:
        return jsonify({"error": error}), 400
    color = params['color']
    alternate_color = params['alternate_color']
    count = params['count']
    wait = params['wait']
    fade_steps = params['fade_steps']
    if not isinstance(color, list) or len(color) != 3 or not isinstance(alternate_color, list) or len(alternate_color) != 3:
        return jsonify({"error": "Invalid colors. Provide lists of three integers for 'color' and 'alternate_color'."}), 400
    try:
        color = [int(c) for c in color]
        alternate_color = [int(c) for c in alternate_color]
        count = int(count)
        wait = float(wait)
        fade_steps = int(fade_steps)
    except ValueError:
        return jsonify({"error": "Invalid parameters. Ensure colors are integers and count, fade_steps are integers, wait is float."}), 400
    update_database('sparkle_effect', {
        "color": color,
        "alternate_color": alternate_color,
        "count": count,
        "wait": wait,
        "fade_steps": fade_steps
    })
    return jsonify({
        "status": "Sparkle effect parameters saved.",
        "color": color,
        "alternate_color": alternate_color,
        "count": count,
        "wait": wait,
        "fade_steps": fade_steps
    }), 200

@app.route('/set_brightness', methods=['POST'])
def api_set_brightness():
    data = request.get_json()
    params, error = extract_api_parameters(data, ['brightness'])
    if error:
        return jsonify({"error": error}), 400
    brightness = params['brightness']
    try:
        brightness = float(brightness)
        if not (0.0 <= brightness <= 1.0):
            raise ValueError
    except ValueError:
        return jsonify({"error": "Brightness must be a float between 0.0 and 1.0."}), 400
    update_database('set_brightness', {"brightness": brightness})
    return jsonify({"status": "Brightness parameter saved.", "brightness": brightness}), 200

@app.route('/stop', methods=['POST'])
def api_stop():
    update_database('stop', {})
    return jsonify({"status": "Stop command saved."}), 200

# New APIs for database interaction
@app.route('/write', methods=['POST'])
def api_write():
    data = request.get_json()
    key = data.get('key')
    value = data.get('value')
    if key is None or value is None:
        return jsonify({"error": "Both 'key' and 'value' are required."}), 400
    with DATABASE_LOCK:
        db = load_database()
        db.setdefault('custom_keys', {})[key] = value
        save_database(db)
    return jsonify({"status": f"Key '{key}' written successfully.", "key": key, "value": value}), 200

@app.route('/retrieve', methods=['POST'])
def api_retrieve():
    data = request.get_json()
    keys = data.get('keys')
    if not isinstance(keys, list):
        return jsonify({"error": "'keys' must be a list of keys to retrieve."}), 400
    retrieved = get_from_database(keys)
    return jsonify({"retrieved": retrieved}), 200

@app.route('/delete', methods=['POST'])
def api_delete():
    data = request.get_json()
    keys = data.get('keys')
    if not isinstance(keys, list):
        return jsonify({"error": "'keys' must be a list of keys to delete."}), 400
    remove_from_database(keys)
    return jsonify({"status": f"Keys {keys} deleted successfully."}), 200

if __name__ == '__main__':
    try:
        # Initialize the database file if it doesn't exist
        with DATABASE_LOCK:
            load_database()
        app.run(host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        pass
