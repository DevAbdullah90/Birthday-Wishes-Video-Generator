import requests
import os

def download_file(url, output_path):
    response = requests.get(url, stream=True)
    with open(output_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    print(f"Downloaded file to: {output_path}")

# Create assets directory if it doesn't exist
os.makedirs("assets", exist_ok=True)

# URL to a free music file (change this URL to a different royalty-free music if needed)
url = "https://cdn.pixabay.com/download/audio/2021/11/25/audio_cb15806492.mp3?filename=happy-birthday-to-you-piano-music-for-birthday-video-background-music-132819.mp3"
output_path = os.path.join("assets", "bg_music.mp3")

download_file(url, output_path)
print("Background music downloaded successfully!") 