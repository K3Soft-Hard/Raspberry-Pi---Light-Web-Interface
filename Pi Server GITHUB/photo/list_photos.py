import os
import json

# Settings
IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif', '.webp')
image_folder = os.path.dirname(os.path.realpath(__file__))

images = []
for file in os.listdir(image_folder):
    if file.lower().endswith(IMAGE_EXTENSIONS):
        images.append(file)

with open(os.path.join(image_folder, 'images.json'), 'w') as f:
    json.dump(images, f)

print(f"Scanned {len(images)} images.")