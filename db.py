import json
import os

from server import DATABASE_FILE, DATABASE_LOCK

def load_database():
    """Load the database from the JSON file."""
    if not os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, 'w') as f:
            json.dump({}, f)
    with open(DATABASE_FILE, 'r') as f:
        try:
            data = json.load(f)
            return data
        except json.JSONDecodeError:
            return {}

def save_database(data):
    """Save the database to the JSON file."""
    with open(DATABASE_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def update_database(key, value):
    """Update a specific key in the database."""
    with DATABASE_LOCK:
        db = load_database()
        db[key] = value
        save_database(db)

def remove_from_database(keys):
    """Remove specific keys from the database."""
    with DATABASE_LOCK:
        db = load_database()
        for key in keys:
            db.pop(key, None)
        save_database(db)

def get_from_database(keys):
    """Retrieve specific keys from the database."""
    with DATABASE_LOCK:
        db = load_database()
        return {key: db.get(key) for key in keys}
