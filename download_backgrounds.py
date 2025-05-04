import requests
import os

def download_file(url, output_path):
    response = requests.get(url, stream=True)
    with open(output_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    print(f"Downloaded file to: {output_path}")

# Create backgrounds directory if it doesn't exist
os.makedirs("assets/backgrounds", exist_ok=True)

# URLs to free background images (royalty-free from Pixabay/Pexels)
background_urls = [
    # Balloons
    "https://cdn.pixabay.com/photo/2016/11/23/18/06/balloons-1854225_1280.jpg",
    # Confetti
    "https://cdn.pixabay.com/photo/2016/09/10/13/39/pink-1659113_1280.jpg",
    # Birthday cake
    "https://cdn.pixabay.com/photo/2016/11/22/18/52/cake-1850011_1280.jpg",
    # Gift box
    "https://cdn.pixabay.com/photo/2017/12/13/00/23/christmas-3015776_1280.jpg"
]

# Download each background image
for i, url in enumerate(background_urls):
    output_path = os.path.join("assets/backgrounds", f"background_{i+1}.jpg")
    download_file(url, output_path)

print("Background images downloaded successfully!") 