import requests
import os

def download_file(url, output_path):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        print(f"Downloaded file to: {output_path}")
        print(f"File size: {os.path.getsize(output_path)} bytes")
        return True
    else:
        print(f"Failed to download file: {response.status_code}")
        return False

# Create assets directory if it doesn't exist
os.makedirs("assets", exist_ok=True)

# Try multiple URLs in case one fails - prioritize birthday themed music
music_urls = [
    # Birthday music options
    "https://files.freemusicarchive.org/storage-freemusicarchive-org/music/Music_for_Video/Podington_Bear/Solo_Instruments/Podington_Bear_-_Happy_Birthday.mp3",
    "https://cdn.pixabay.com/download/audio/2021/11/25/audio_cb15806492.mp3?filename=happy-birthday-to-you-piano-music-for-birthday-video-background-music-132819.mp3",
    "https://www.chosic.com/wp-content/uploads/2020/07/purrple-cat-equinox.mp3",
    "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
    "https://filesamples.com/samples/audio/mp3/sample3.mp3"
]

output_path = os.path.join("assets", "bg_music.mp3")

# Try each URL until one works
for url in music_urls:
    print(f"Trying to download from: {url}")
    if download_file(url, output_path):
        print("Background music downloaded successfully!")
        break
else:
    print("Failed to download background music from any source.") 