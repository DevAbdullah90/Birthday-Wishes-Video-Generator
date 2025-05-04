import os
import moviepy
from PIL import Image

print(f"Moviepy version: {moviepy.__version__}")

# Test creating a ColorClip
try:
    from moviepy.video.VideoClip import ColorClip
    color_clip = ColorClip(size=(720, 480), color=(255, 0, 0), duration=5)
    print("ColorClip creation successful")
    print(f"ColorClip methods: {dir(color_clip)}")
except Exception as e:
    print(f"ColorClip error: {e}")

# Test creating a TextClip
try:
    from moviepy.video.VideoClip import TextClip
    text_clip = TextClip(txt="Test Text", fontsize=30, color="white")
    if hasattr(text_clip, 'set_duration'):
        text_clip = text_clip.set_duration(5)
    elif hasattr(text_clip, 'duration'):
        text_clip.duration = 5
    else:
        print("No duration setting method found for TextClip")
    print("TextClip creation successful")
    print(f"TextClip methods: {dir(text_clip)}")
except Exception as e:
    print(f"TextClip error: {e}")

# Test creating an ImageClip
if not os.path.exists('test_image.jpg'):
    # Create a simple test image
    img = Image.new('RGB', (100, 100), color=(73, 109, 137))
    img.save('test_image.jpg')

try:
    from moviepy.video.VideoClip import ImageClip
    img_clip = ImageClip('test_image.jpg')
    if hasattr(img_clip, 'set_duration'):
        img_clip = img_clip.set_duration(5)
    elif hasattr(img_clip, 'duration'):
        img_clip.duration = 5
    else:
        print("No duration setting method found for ImageClip")
    print("ImageClip creation successful")
    print(f"ImageClip methods: {dir(img_clip)}")
except Exception as e:
    print(f"ImageClip error: {e}")

# Test creating a CompositeVideoClip
try:
    from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
    composite = CompositeVideoClip([color_clip])
    print("CompositeVideoClip creation successful")
    print(f"CompositeVideoClip methods: {dir(composite)}")
except Exception as e:
    print(f"CompositeVideoClip error: {e}") 