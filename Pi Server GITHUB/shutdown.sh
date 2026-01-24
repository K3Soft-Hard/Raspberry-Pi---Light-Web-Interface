#!/bin/bash
echo "Stopping Web Server and Shutting Down..."
# Kills any python process running the editor (optional but cleaner)
pkill -f editor_api.py
# Execute the system shutdown
sudo shutdown now