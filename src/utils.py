import random
import json
from datetime import datetime
import os

def get_random_proxy(proxies):
    proxy = random.choice(proxies)
    return {
        "http": proxy,
        "https": proxy.replace("http://", "https://")
    }

def format_proxy_list(raw_proxies):
    formatted = []
    for proxy in raw_proxies.strip().split('\n'):
        if proxy:
            ip, port, username, password = proxy.strip().split(':')
            formatted_proxy = f"http://{username}:{password}@{ip}:{port}"
            formatted.append(formatted_proxy)
    return formatted

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
