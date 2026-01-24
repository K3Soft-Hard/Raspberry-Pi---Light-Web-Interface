#!/bin/bash
# 1. Get the current directory
MAIN_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$MAIN_DIR"

echo "--- 1. SCANNING VIDEOS ---"
if cd "$MAIN_DIR/video"; then
    python3 list_videos.py
    cd "$MAIN_DIR"
fi

echo "--- 2. SCANNING PHOTOS ---"
if cd "$MAIN_DIR/photo"; then
    python3 list_photos.py
    cd "$MAIN_DIR"
fi

# 3. Kill any old server on port 8000
echo "--- 3. RESETTING SERVER ---"
fuser -k 8000/tcp > /dev/null 2>&1

# 4. Start the Editor/Media Server
echo "--- 4. SYSTEM READY ---"
echo "Editor: http://localhost:8000/editor.html"
echo "Videos: http://localhost:8000/video/index.html"
echo "Photos: http://localhost:8000/photo/gallery.html"
python3 editor_api.py