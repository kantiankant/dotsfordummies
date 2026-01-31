#!/usr/bin/env python3

import requests
import time
import sys
import os
from datetime import datetime
import threading
import select

class WeatherTUI:
    def __init__(self):
        self.running = True
        self.weather_data = None
        self.last_update = None
        self.error_msg = None
        self.update_interval = 60  # seconds
        
    def fetch_weather(self):
        """Fetch weather data from Open-Meteo API"""
        try:
            url = "https://api.open-meteo.com/v1/forecast"
            params = {
                "latitude": 1.3521,
                "longitude": 103.8198,
                "current": "temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,cloud_cover,wind_speed_10m,wind_direction_10m",
                "timezone": "Asia/Singapore"
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            self.weather_data = data['current']
            self.last_update = datetime.now()
            self.error_msg = None
            return True
            
        except Exception as e:
            self.error_msg = f"Failed to fetch weather: {str(e)}"
            return False
    
    def get_weather_description(self, code):
        """Convert weather code to description"""
        descriptions = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Foggy", 48: "Foggy",
            51: "Light drizzle", 53: "Light drizzle", 55: "Light drizzle",
            61: "Rainy", 63: "Rainy", 65: "Rainy",
            71: "Snowy", 73: "Snowy", 75: "Snowy",
            77: "Snow grains",
            80: "Rain showers", 81: "Rain showers", 82: "Rain showers",
            85: "Snow showers", 86: "Snow showers",
            95: "Thunderstorm",
            96: "Thunderstorm with hail", 99: "Thunderstorm with hail"
        }
        return descriptions.get(code, "Unknown conditions")
    
    def get_weather_emoji(self, code):
        """Get emoji for weather code"""
        if code == 0:
            return "☀️"
        elif code in [1, 2]:
            return "🌤️"
        elif code == 3:
            return "☁️"
        elif code in [45, 48]:
            return "🌫️"
        elif code in [51, 53, 55, 61, 63, 65, 80, 81, 82]:
            return "🌧️"
        elif code in [95, 96, 99]:
            return "⛈️"
        elif code in [71, 73, 75, 77, 85, 86]:
            return "❄️"
        else:
            return "🌤️"
    
    def wind_direction(self, deg):
        """Convert wind degree to direction"""
        directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
        idx = int((deg + 22.5) / 45) % 8
        return directions[idx]
    
    def clear_screen(self):
        """Clear terminal screen"""
        os.system('clear' if os.name != 'nt' else 'cls')
    
    def display_weather(self):
        """Display weather information"""
        self.clear_screen()
        
<<<<<<< HEAD
        print("╔══════════════════════════════════════════════╗")
        print("║     Singapore Weather - Live Updates         ║")
        print("╚══════════════════════════════════════════════╝")
        print()
=======
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
>>>>>>> refs/remotes/origin/main
        
        if self.error_msg:
            print(f"⚠️  Error: {self.error_msg}")
            print()
        
        if self.weather_data:
            code = self.weather_data['weather_code']
            desc = self.get_weather_description(code)
            emoji = self.get_weather_emoji(code)
            
            print(f"  {emoji} {desc}")
            print()
            
            print(f"  🌡️  Temperature:  {self.weather_data['temperature_2m']:.1f}°C")
            print(f"  🤔 Feels like:    {self.weather_data['apparent_temperature']:.1f}°C")
            print(f"  💧 Humidity:      {self.weather_data['relative_humidity_2m']}%")
            print(f"  ☁️  Cloud cover:   {self.weather_data['cloud_cover']}%")
            print(f"  💨 Wind speed:    {self.weather_data['wind_speed_10m']:.1f} km/h")
            
            wind_dir = self.wind_direction(self.weather_data['wind_direction_10m'])
            print(f"  🧭 Wind direction: {wind_dir} ({self.weather_data['wind_direction_10m']}°)")
            print()
            
            print("  📍 Location: Singapore")
            if self.last_update:
                print(f"  🕐 Last updated: {self.last_update.strftime('%H:%M:%S')}")
            print()
        
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("  Press 'q' or Ctrl+C to exit")
        print(f"  Updates every {self.update_interval} seconds")
    
    def check_input(self):
        """Check for keyboard input (non-blocking)"""
        if os.name == 'nt':  # Windows
            import msvcrt
            if msvcrt.kbhit():
                key = msvcrt.getch().decode('utf-8').lower()
                if key == 'q':
                    self.running = False
        else:  # Unix/Linux/Mac
            if select.select([sys.stdin], [], [], 0)[0]:
                key = sys.stdin.read(1).lower()
                if key == 'q':
                    self.running = False
    
    def run(self):
        """Main loop"""
        # Set terminal to non-blocking mode on Unix
        if os.name != 'nt':
            import tty
            import termios
            old_settings = termios.tcgetattr(sys.stdin)
            try:
                tty.setcbreak(sys.stdin.fileno())
                
                # Initial fetch
                self.fetch_weather()
                self.display_weather()
                
                last_fetch = time.time()
                
                while self.running:
                    current_time = time.time()
                    
                    # Update weather data
                    if current_time - last_fetch >= self.update_interval:
                        self.fetch_weather()
                        self.display_weather()
                        last_fetch = current_time
                    
                    # Check for quit key
                    self.check_input()
                    
                    time.sleep(0.1)
                
            except KeyboardInterrupt:
                pass
            finally:
                termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
                self.clear_screen()
        else:
            # Windows version
            try:
                self.fetch_weather()
                self.display_weather()
                
                last_fetch = time.time()
                
                while self.running:
                    current_time = time.time()
                    
                    if current_time - last_fetch >= self.update_interval:
                        self.fetch_weather()
                        self.display_weather()
                        last_fetch = current_time
                    
                    self.check_input()
                    time.sleep(0.1)
                    
            except KeyboardInterrupt:
                pass
            finally:
                self.clear_screen()

if __name__ == "__main__":
    tui = WeatherTUI()
    tui.run()
