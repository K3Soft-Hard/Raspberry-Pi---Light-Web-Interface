import os
import json

# Settings: Add any formats you use
VIDEO_EXTENSIONS = ('.mp4', '.webm', '.ogg', '.mkv', '.mov')
video_folder = os.path.dirname(os.path.realpath(__file__)) # Gets the folder where THIS script is

videos = []
for file in os.listdir(video_folder):
    if file.lower().endswith(VIDEO_EXTENSIONS):
        videos.append(file)

# Save the list to a JSON file (Fixed 'w' mode)
json_path = os.path.join(video_folder, 'videos.json')
with open(json_path, 'w') as f:
    json.dump(videos, f)

print(f"--- SCAN COMPLETE ---")
print(f"Found {len(videos)} videos")
print(f"File saved to: {json_path}")