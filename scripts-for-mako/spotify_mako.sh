#!/usr/bin/env bash

# Wait for Wayland to be ready
while [ -z "$WAYLAND_DISPLAY" ]; do
  sleep 1
done

# Start the listener
playerctl -p spotify metadata --format '{{title}} - {{artist}}' --follow | while read -r line; do
  # -a "Music" ensures it bypasses your [app-name=Spotify] invisible rule
  notify-send -a "Music" "Now Playing" "$line" --icon=spotify
done
