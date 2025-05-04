import streamlit as st

# Streamlit configuration must be the first Streamlit command
st.set_page_config(page_title="Birthday Wishes Video Generator", layout="centered")

import tempfile
import os
import shutil
import glob
import random
from PIL import Image
import numpy as np

# Import moviepy components
try:
    import moviepy
    # Fix moviepy import structure
    from moviepy.video.VideoClip import ColorClip
    from moviepy.video.VideoClip import ImageClip
    from moviepy.video.VideoClip import TextClip
    from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
    from moviepy.audio.io.AudioFileClip import AudioFileClip
    # Remove problematic import
except ImportError as e:
    st.error(f"Error importing moviepy: {str(e)}")

st.title("🎉 Birthday Wishes Video Generator")
st.markdown("Create beautiful birthday videos with music, transitions, and your photos!")

# User inputs
name = st.text_input("Recipient's Name", placeholder="Enter name here...")
message = st.text_area("Custom Message", "Wishing you a wonderful birthday filled with joy and surprises!")

# Allow multiple image uploads
uploaded_images = st.file_uploader("Upload Photos (up to 5)", type=["jpg", "png", "jpeg"], accept_multiple_files=True)

# Theme selection with descriptions
theme_descriptions = {
    "Classic": "Pink and white theme with elegant transitions",
    "Romantic": "Soft pink theme with heart decorations",
    "Fun": "Bright, colorful theme with confetti effects"
}
theme = st.selectbox("Choose Theme", list(theme_descriptions.keys()))
st.caption(theme_descriptions[theme])

# Video duration
duration = st.slider("Video Duration (seconds)", min_value=5, max_value=30, value=15, step=5)

# Music options
st.subheader("🎵 Background Music")
music_choice = st.radio(
    "Choose background music:",
    ["Default", "Birthday Song", "Happy Tune", "None"],
    horizontal=True
)

# Option to download new birthday music
if st.button("🎵 Update Background Music"):
    with st.spinner("Downloading new background music..."):
        try:
            import subprocess
            
            # Determine which music type to download based on user selection
            music_type = "default"
            if music_choice == "Birthday Song":
                music_type = "birthday"
            elif music_choice == "Happy Tune":
                music_type = "happy"
            
            # Run the get_music.py script with the selected music type
            result = subprocess.run(["python", "get_music.py", music_type], capture_output=True, text=True)
            st.success(f"{music_choice} music updated successfully!")
            st.info(result.stdout)
        except Exception as e:
            st.error(f"Error updating music: {str(e)}")

# Video generation button
generate = st.button("🎬 Generate Birthday Video")

# Function to generate video
def create_video(name, message, uploaded_images, theme, duration):
    try:
        # Create a temp directory for processing
        temp_dir = tempfile.mkdtemp()
        
        # Theme-based colors
        theme_colors = {
            "Classic": (255, 204, 229),  # Pink
            "Romantic": (255, 192, 203),  # Light Pink
            "Fun": (255, 255, 0)  # Yellow
        }
        
        # Base video parameters
        W, H = 1280, 720  # HD video size
        
        # Process uploaded images (limit to 5)
        image_paths = []
        if uploaded_images:
            for i, img_file in enumerate(uploaded_images[:5]):
                # Save uploaded image to temp directory
                img = Image.open(img_file)
                img = img.convert('RGB')  # Convert to RGB to avoid transparency issues
                
                # Resize to fit video dimensions while maintaining aspect ratio
                img_w, img_h = img.size
                ratio = min(W / img_w, H / img_h)
                new_size = (int(img_w * ratio), int(img_h * ratio))
                img = img.resize(new_size, Image.LANCZOS)
                
                # Save to temp directory
                img_path = os.path.join(temp_dir, f"user_image_{i}.jpg")
                img.save(img_path)
                image_paths.append(img_path)
        
        # Get background images for slideshow if not enough user images
        background_folder = os.path.join("assets", "backgrounds")
        background_images = []
        if os.path.exists(background_folder):
            background_images = glob.glob(os.path.join(background_folder, "*.jpg"))
        
        # If we have fewer than 3 images (including user uploads), add background images
        all_images = image_paths.copy()
        if background_images and len(all_images) < 3:
            remaining_slots = 3 - len(all_images)
            random.shuffle(background_images)
            all_images.extend(background_images[:remaining_slots])
        
        # Base clip - use color background
        color_bg = ColorClip(size=(W, H), color=theme_colors.get(theme, (255, 204, 229)), duration=duration)
        
        # All clips will be added to this list
        all_clips = [color_bg]
        
        # If we have images, add them to the video at different positions
        if all_images:
            # Calculate position for each image in the timeline
            for i, img_path in enumerate(all_images):
                # Load image with PIL first to resize properly
                pil_img = Image.open(img_path)
                
                # Resize to fit video height while maintaining aspect ratio
                img_w, img_h = pil_img.size
                ratio = H / img_h
                new_size = (int(img_w * ratio), H)
                pil_img = pil_img.resize(new_size, Image.LANCZOS)
                
                # Save the resized image
                resized_path = os.path.join(temp_dir, f"resized_{os.path.basename(img_path)}")
                pil_img.save(resized_path)
                
                # Create ImageClip from the resized image
                # For multiple images, stagger their start times across the video duration
                image_start = i * (duration / len(all_images))
                image_duration = duration / len(all_images) * 1.5  # Overlap images slightly
                
                # Make sure the duration doesn't exceed the total video duration
                if image_start + image_duration > duration:
                    image_duration = duration - image_start
                
                img_clip = ImageClip(resized_path).with_duration(image_duration)
                img_clip = img_clip.with_position(("center", "center"))
                # Set start time in the video
                img_clip = img_clip.with_start(image_start)
                
                all_clips.append(img_clip)
        
        # Create text clips for name and message
        try:
            # Title text (name)
            title_text = TextClip(
                text=f"Happy Birthday {name}!",
                fontsize=70, 
                color='white', 
                font="Arial",
                method='label'
            ).with_duration(duration)
            
            # Add shadow effect to make text more readable
            shadow = TextClip(
                text=f"Happy Birthday {name}!",
                fontsize=70, 
                color='black', 
                font="Arial",
                method='label'
            ).with_duration(duration)
            
            # Position shadow slightly offset
            shadow = shadow.with_position(("center", 140 + 2))
            
            # Position title text
            title_text = title_text.with_position(("center", 140))
            
            # Message text
            msg_text = TextClip(
                text=message,
                fontsize=40, 
                color='white', 
                font="Arial",
                method='label'
            ).with_duration(duration)
            
            # Add shadow effect to message
            msg_shadow = TextClip(
                text=message,
                fontsize=40, 
                color='black', 
                font="Arial",
                method='label'
            ).with_duration(duration)
            
            # Position shadow and message
            msg_shadow = msg_shadow.with_position(("center", 550 + 2))
            msg_text = msg_text.with_position(("center", 550))
            
            # Add all text elements to the clip list
            all_clips.extend([shadow, title_text, msg_shadow, msg_text])
            
        except Exception as e:
            st.warning(f"Error creating text: {str(e)}")
            import traceback
            st.warning(traceback.format_exc())
        
        # Combine all clips
        final_video = CompositeVideoClip(all_clips, size=(W, H))
        final_video = final_video.with_duration(duration)
        
        # Add background music
        try:
            if music_choice == "None":
                st.info("No background music selected.")
            else:
                audio_path = os.path.join("assets", "bg_music.mp3")
                if os.path.exists(audio_path) and os.path.getsize(audio_path) > 1000:  # Make sure file exists and is not empty
                    st.info(f"Adding {music_choice} background music")
                    
                    # Load audio file
                    audio = AudioFileClip(audio_path)
                    
                    # Use with_duration to set the audio length instead of subclip
                    if hasattr(audio, 'duration') and audio.duration > duration:
                        st.info(f"Audio duration: {audio.duration}s, video duration: {duration}s")
                        audio = audio.with_duration(duration)
                    
                    # Use with_volume_scaled method which should exist
                    if hasattr(audio, 'with_volume_scaled'):
                        audio = audio.with_volume_scaled(0.5)  # Lower volume to 50%
                    
                    # Add audio to video
                    final_video = final_video.with_audio(audio)
                    st.success("Background music added successfully!")
                else:
                    st.warning(f"Background music file not found or invalid.")
                    if music_choice != "None":
                        st.info(f"Attempting to download {music_choice} music...")
                        
                        # Try to download music using our music script
                        try:
                            import subprocess
                            
                            # Determine which music type to download
                            music_type = "default"
                            if music_choice == "Birthday Song":
                                music_type = "birthday"
                            elif music_choice == "Happy Tune":
                                music_type = "happy"
                            
                            # Run the get_music.py script with the selected music type
                            subprocess.run(["python", "get_music.py", music_type], check=True)
                            
                            # Check if download was successful
                            if os.path.exists(audio_path) and os.path.getsize(audio_path) > 1000:
                                audio = AudioFileClip(audio_path)
                                # Use with_duration to trim audio
                                if hasattr(audio, 'duration') and audio.duration > duration:
                                    audio = audio.with_duration(duration)
                                # Lower volume
                                if hasattr(audio, 'with_volume_scaled'):
                                    audio = audio.with_volume_scaled(0.5)
                                final_video = final_video.with_audio(audio)
                                st.success(f"{music_choice} music added to video!")
                            else:
                                st.warning("Could not download background music. Video will be generated without audio.")
                        except Exception as e:
                            st.warning(f"Error downloading music: {str(e)}. Video will be generated without audio.")
        except Exception as e:
            st.warning(f"Error adding audio: {str(e)}")
            import traceback
            st.warning(traceback.format_exc())
        
        # Create output directory if it doesn't exist
        os.makedirs("output", exist_ok=True)
        
        # Generate unique filename
        output_path = os.path.join("output", f"birthday_video_{name.replace(' ', '_')}_{random.randint(1000, 9999)}.mp4")
        
        # Write the video file
        final_video.write_videofile(output_path, fps=24, codec="libx264", audio_codec='aac')
        
        # Clean up temporary files
        try:
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
        except Exception as e:
            st.warning(f"Error cleaning up temporary files: {str(e)}")
            
        return output_path
        
    except Exception as e:
        st.error(f"Error generating video: {str(e)}")
        import traceback
        st.error(traceback.format_exc())
        return None

# Handling video generation and display
if generate:
    if not name:
        st.warning("Please enter the recipient's name.")
    else:
        with st.spinner("🎥 Generating your birthday video... This may take a moment."):
            video_path = create_video(name, message, uploaded_images, theme, duration)
            if video_path:
                st.success("🎉 Your video is ready!")
                st.video(video_path)

                # Provide download button
                with open(video_path, "rb") as file:
                    st.download_button(
                        "📥 Download Video",
                        data=file,
                        file_name=os.path.basename(video_path),
                        mime="video/mp4"
                    )
                
                st.info("Don't forget to download your video if you like it! It will be deleted when you close the browser.")

# Show some example videos
with st.expander("How to create a great birthday video"):
    st.markdown("""
    ### Tips for creating a great birthday video:
    1. **Upload multiple photos** of the birthday person for a personalized slideshow effect
    2. **Write a heartfelt message** that will appear in the video
    3. **Choose a theme** that matches the personality of the birthday person
    4. **Adjust the duration** to fit the number of photos and length of your message
    
    The generated video will include transitions between images, background music, and animated text!
    """)
