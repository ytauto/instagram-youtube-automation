import random
import json
from datetime import datetime
import os

def get_random_proxy(proxies):
    return random.choice(proxies)

def load_processed_reels():
    try:
        with open('processed_reels.json', 'r') as f:
            return json.load(f)
    except:
        return []

def save_processed_reels(processed):
    with open('processed_reels.json', 'w') as f:
        json.dump(processed, f)

def cleanup_temp():
    for file in os.listdir('temp'):
        os.remove(os.path.join('temp', file))
