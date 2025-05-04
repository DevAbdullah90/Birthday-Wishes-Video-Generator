print("Testing moviepy modules...")
try:
    import moviepy
    print(f"Moviepy is installed. Version: {moviepy.__version__}")
    print(f"Available modules: {dir(moviepy)}")
    
    # Try importing from the video module
    try:
        from moviepy.video.io.VideoFileClip import VideoFileClip
        print("VideoFileClip import successful")
    except ImportError as e:
        print(f"VideoFileClip import failed: {e}")
    
    # Try importing from the audio module
    try:
        from moviepy.audio.io.AudioFileClip import AudioFileClip
        print("AudioFileClip import successful")
    except ImportError as e:
        print(f"AudioFileClip import failed: {e}")
    
    # Try importing text components
    try:
        from moviepy.video.VideoClip import TextClip
        print("TextClip import successful")
    except ImportError as e:
        print(f"TextClip import failed: {e}")
        
except ImportError as e:
    print(f"Moviepy import failed: {e}") 