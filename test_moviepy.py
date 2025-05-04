print("Testing moviepy imports...")
try:
    from moviepy.editor import TextClip, ImageClip, AudioFileClip, CompositeVideoClip, ColorClip
    print("All imports successful!")
except ImportError as e:
    print(f"Import Error: {e}")
    print("Trying alternative import method...")
    try:
        import moviepy.editor as editor
        print("Alternative import method successful!")
        print(f"Available modules: {dir(editor)}")
    except ImportError as e:
        print(f"Alternative import also failed: {e}") 