import requests
import os
import sys

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

# Music options
music_options = {
    "birthday": [
        "https://cdn.pixabay.com/download/audio/2021/11/25/audio_cb15806492.mp3?filename=happy-birthday-to-you-piano-music-for-birthday-video-background-music-132819.mp3",
        "https://files.freemusicarchive.org/storage-freemusicarchive-org/music/Music_for_Video/Podington_Bear/Solo_Instruments/Podington_Bear_-_Happy_Birthday.mp3",
        "https://www.tribeofnoise.com/audio/14604/Jingle_Punks_-_Birthday_Brass",
    ],
    "happy": [
        "https://www.chosic.com/wp-content/uploads/2020/07/purrple-cat-equinox.mp3",
        "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3",
        "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
    ],
    "default": [
        "https://filesamples.com/samples/audio/mp3/sample3.mp3",
        "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-7.mp3",
    ]
}

def get_music(music_type="default"):
    # Choose appropriate URLs based on selection
    if music_type.lower() in music_options:
        urls = music_options[music_type.lower()]
    else:
        urls = music_options["default"]
    
    output_path = os.path.join("assets", "bg_music.mp3")
    
    # Try each URL until one works
    for url in urls:
        print(f"Trying to download {music_type} music from: {url}")
        if download_file(url, output_path):
            print(f"{music_type.capitalize()} music downloaded successfully!")
            return True
    
    print("Failed to download music from any source.")
    return False

if __name__ == "__main__":
    # Get music type from command line argument or use default
    music_type = "default"
    if len(sys.argv) > 1:
        music_type = sys.argv[1].lower()
    
    get_music(music_type) 