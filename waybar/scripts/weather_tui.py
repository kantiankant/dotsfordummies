#!/usr/bin/env python3

import requests
import time
import sys
from datetime import datetime

def fetch_weather():
    try:
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": 1.3521,
            "longitude": 103.8198,
            "current": "temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,cloud_cover,wind_speed_10m,wind_direction_10m",
            "timezone": "Asia/Singapore"
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()['current']
    except Exception as e:
        return None

def get_weather_description(code):
    descriptions = {
        0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
        45: "Foggy", 48: "Foggy",
        51: "Light drizzle", 53: "Light drizzle", 55: "Light drizzle",
        61: "Rainy", 63: "Rainy", 65: "Rainy",
        80: "Rain showers", 81: "Rain showers", 82: "Rain showers",
        95: "Thunderstorm", 96: "Thunderstorm with hail", 99: "Thunderstorm with hail"
    }
    return descriptions.get(code, "Unknown conditions")

def get_weather_emoji(code):
    if code == 0: return "☀️"
    elif code in [1, 2]: return "🌤️"
    elif code == 3: return "☁️"
    elif code in [45, 48]: return "🌫️"
    elif code in [51, 53, 55, 61, 63, 65, 80, 81, 82]: return "🌧️"
    elif code in [95, 96, 99]: return "⛈️"
    else: return "🌤️"

def wind_direction(deg):
    directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    idx = int((deg + 22.5) / 45) % 8
    return directions[idx]

def clear_screen():
    print("\033[2J\033[H", end='')

def display_weather(weather_data):
    clear_screen()
    
    code = weather_data['weather_code']
    desc = get_weather_description(code)
    emoji = get_weather_emoji(code)
    
    print("╔══════════════════════════════════════════════╗")
    print("║      Singapore Weather - Live Updates        ║")
    print("╚══════════════════════════════════════════════╝")
    print()
    print(f"  {emoji} {desc}")
    print()
    print(f"  🌡️  Temperature:  {weather_data['temperature_2m']:.1f}°C")
    print(f"  🤔 Feels like:    {weather_data['apparent_temperature']:.1f}°C")
    print(f"  💧 Humidity:      {weather_data['relative_humidity_2m']}%")
    print(f"  ☁️  Cloud cover:   {weather_data['cloud_cover']}%")
    print(f"  💨 Wind speed:    {weather_data['wind_speed_10m']:.1f} km/h")
    
    wind_dir = wind_direction(weather_data['wind_direction_10m'])
    print(f"  🧭 Wind direction: {wind_dir} ({weather_data['wind_direction_10m']}°)")
    print()
    print("  📍 Location: Singapore")
    print(f"  🕐 Last updated: {datetime.now().strftime('%H:%M:%S')}")
    print()
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("  Press 'q' or Ctrl+C to exit")
    print("  Updates every 30 seconds")
    
    sys.stdout.flush()

def main():
    # Hide cursor
    print("\033[?25l", end='')
    sys.stdout.flush()
    
    try:
        last_update = 0
        weather_data = None
        
        while True:
            current_time = time.time()
            
            # Update every 30 seconds or on first run
            if weather_data is None or current_time - last_update >= 30:
                weather_data = fetch_weather()
                if weather_data:
                    display_weather(weather_data)
                    last_update = current_time
            
            time.sleep(1)
            
    except KeyboardInterrupt:
        pass
    finally:
        # Show cursor
        print("\033[?25h", end='')
        sys.stdout.flush()

if __name__ == "__main__":
    main()
