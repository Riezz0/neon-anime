#!/usr/bin/env python3

import requests
import json
from datetime import datetime
from pathlib import Path
import sys

# Configuration for Johannesburg
CITY = "Johannesburg"
COUNTRY = "South Africa"
METHOD = 3  # 3 = Shafi'i (MWL) calculation method
TIMEZONE = "Africa/Johannesburg"
CACHE_FILE = Path.home() / ".cache" / "prayer_times.json"

def fetch_prayer_times():
    """Fetch prayer times from API with error handling"""
    try:
        url = f"http://api.aladhan.com/v1/timingsByCity?city={CITY}&country={COUNTRY}&method={METHOD}&school=0"
        response = requests.get(url, timeout=5)
        data = response.json()
        
        if data.get('code') == 200:
            # Cache the successful response
            with open(CACHE_FILE, 'w') as f:
                json.dump(data, f)
            return data['data']['timings']
        return None
    except Exception as e:
        print(f"API Error: {e}", file=sys.stderr)
        return None

def get_cached_times():
    """Get cached prayer times if available"""
    try:
        if CACHE_FILE.exists():
            with open(CACHE_FILE) as f:
                data = json.load(f)
                return data['data']['timings']
    except Exception as e:
        print(f"Cache Error: {e}", file=sys.stderr)
    return None

def format_output(prayer_times):
    """Format the output for Waybar"""
    now = datetime.now().strftime('%H:%M')
    prayers_order = ['Fajr', 'Sunrise', 'Dhuhr', 'Asr', 'Maghrib', 'Isha']
    prayers = [(name, prayer_times[name]) for name in prayers_order if name in prayer_times]
    
    current = next_prayer = None
    for i in range(len(prayers)):
        if prayers[i][1] <= now:
            current = prayers[i]
            next_prayer = prayers[i + 1] if i < len(prayers) - 1 else prayers[0]
        elif not next_prayer:
            next_prayer = prayers[i]
    
    current = current or prayers[-1]  # Before Fajr shows Isha as last
    next_prayer = next_prayer or prayers[0]  # After Isha shows Fajr next
    
    return {
        'text': f" {current[0]}: {current[1]} | Next: {next_prayer[0]}: {next_prayer[1]}",
        'tooltip': "\n".join([f"{p}: {t}" for p, t in prayer_times.items() if p in prayers_order]),
        'class': 'prayer-times'
    }

def main():
    # Try to fetch fresh times, fall back to cache if needed
    prayer_times = fetch_prayer_times() or get_cached_times()
    
    if not prayer_times:
        print(json.dumps({
            'text': "⛔ Prayer Times Error",
            'tooltip': "Failed to fetch prayer times. Check internet connection.",
            'class': 'error'
        }))
        return
    
    print(json.dumps(format_output(prayer_times)))

if __name__ == "__main__":
    main()
