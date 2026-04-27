import json
import os

SETTINGS_FILE = "settings.json"
LEADERBOARD_FILE = "leaderboard.json"


def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        return {"sound": True, "car_color": "red", "difficulty": "medium"}
    with open(SETTINGS_FILE) as f:
        return json.load(f)


def save_settings(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)


def load_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        return []
    with open(LEADERBOARD_FILE) as f:
        return json.load(f)


def save_leaderboard(lb):
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(lb, f, indent=4)


def update_leaderboard(lb, entry):
    lb.append(entry)
    lb = sorted(lb, key=lambda x: x["score"], reverse=True)
    return lb[:10]