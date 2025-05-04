import os
from moviepy.audio.io.AudioFileClip import AudioFileClip

def test_audio(audio_path):
    if not os.path.exists(audio_path):
        print(f"Audio file not found: {audio_path}")
        return
    
    print(f"Testing audio file: {audio_path}")
    print(f"File size: {os.path.getsize(audio_path)} bytes")
    
    try:
        audio = AudioFileClip(audio_path)
        print(f"Successfully loaded audio clip")
        print(f"Audio duration: {audio.duration}")
        print(f"Audio fps: {audio.fps}")
        
        # Test available methods
        print("\nAvailable attributes and methods:")
        for attr in dir(audio):
            if not attr.startswith('_'):
                print(f"- {attr}")
    except Exception as e:
        print(f"Error loading audio: {str(e)}")
        import traceback
        print(traceback.format_exc())

if __name__ == "__main__":
    audio_path = os.path.join("assets", "bg_music.mp3")
    test_audio(audio_path) 