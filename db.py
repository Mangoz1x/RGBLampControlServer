import json
import os
import threading

database = {}

def update_database(key, value):
    """Update a specific key in the database."""
    database[key] = value

def remove_from_database(keys):
    """Remove specific keys from the database."""
    for key in keys:
        database.pop(key, None)

def get_from_database(keys):
    """Retrieve specific keys from the database."""
    return {key: database.get(key) for key in keys}
