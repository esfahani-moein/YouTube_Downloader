from pytubefix import YouTube
from pytubefix.cli import on_progress
import os
import subprocess
import shutil
import sys

from utils.request_patch import apply_request_patch
from utils.file_info import create_safe_filename, format_size
from utils.video_merge import merge_video_audio
from utils.cleanup import rename_and_cleanup

# Loading Heaser for YT
apply_request_patch()

# YouTube Video URL

url = "specify your youtube video url here"

download_dir = r"specify your download directory here" 
path_ffmpeg = r"C:\ffmpeg\ffmpeg-master-latest-win64-gpl-shared\bin\ffmpeg.exe"
os.makedirs(download_dir, exist_ok=True)

# Create YouTube object with progress callback
yt = YouTube(url, on_progress_callback=on_progress)
yt_file_name = create_safe_filename(yt.title)

# Print YouTube Information
print(f"Title: {yt.title}")
print(f"Channel: {yt.author}")
print(f"Length: {yt.length} seconds")
print(f"Views: {yt.views:,}")
print(f"Download directory: {download_dir}")

# Get progressive streams (includes both video and audio)
progressive_streams = yt.streams.filter(progressive=True).order_by('resolution')

# Print available progressive qualities
print("\nAvailable progressive video qualities (video+audio combined):")
for i, stream in enumerate(progressive_streams, 1):
    file_size = format_size(stream.filesize)
    print(f"{i}. Resolution: {stream.resolution}, "
          f"Format: {stream.mime_type}, "
          f"Size: {file_size}, "
          f"FPS: {stream.fps}")




# Get adaptive streams (higher quality, video only)
print("\nHigher quality video-only streams (requires separate audio):")
video_streams = yt.streams.filter(adaptive=True, only_video=True).order_by('resolution')
for i, stream in enumerate(video_streams, 1):
    file_size = format_size(stream.filesize)
    print(f"{i}. Resolution: {stream.resolution}, "
          f"Format: {stream.mime_type}, "
          f"Size: {file_size}, "
          f"FPS: {stream.fps}")



# Get user's choice for video quality
while True:
    try:
        video_choice = input("\nSelect video quality (enter number, or press Enter for highest quality): ")
        
        # Default to highest quality if user just presses Enter
        if video_choice.strip() == "":
            selected_video = video_streams.last()
            print(f"Selected highest quality: {selected_video.resolution}")
            break
        
        # Check for cancel option
        if video_choice.lower() == 'c':
            print("Download process cancelled by user.")
            sys.exit(0)  # Exit the program cleanly
        
        # Convert to integer and validate
        choice_index = int(video_choice) - 1
        if 0 <= choice_index < len(video_streams):
            selected_video = video_streams[choice_index]
            print(f"Selected: {selected_video.resolution}")
            break
        else:
            print(f"Invalid choice. Please enter a number between 1 and {len(video_streams)}.")
    except ValueError:
        print("Please enter a valid number.")



# Print audio-only options
print("\nAudio-only options:")
audio_streams = yt.streams.filter(only_audio=True,file_extension='mp4').order_by('abr')
for i, stream in enumerate(audio_streams, 1):
    file_size = format_size(stream.filesize)
    print(f"{i}. Bitrate: {stream.abr}, "
          f"Format: {stream.mime_type}, "
          f"Size: {file_size}")



# Get user's choice for audio quality
while True:
    try:
        audio_choice = input("\nSelect audio quality (enter number, or press Enter for highest quality): ")
        
        # Default to highest quality if user just presses Enter
        if audio_choice.strip() == "":
            selected_audio = audio_streams.last()
            print(f"Selected highest quality audio: {selected_audio.abr}")
            break
            
        # Convert to integer and validate
        choice_index = int(audio_choice) - 1
        if 0 <= choice_index < len(audio_streams):
            selected_audio = audio_streams[choice_index]
            print(f"Selected: {selected_audio.abr}")
            break
        else:
            print(f"Invalid choice. Please enter a number between 1 and {len(audio_streams)}.")
    except ValueError:
        print("Please enter a valid number.")



# Use selected streams instead of best_video and best_audio
print(f"\nSelected video quality: {selected_video.resolution} ({format_size(selected_video.filesize)})")
print(f"Selected audio quality: {selected_audio.abr} ({format_size(selected_audio.filesize)})")

# Then modify your download code to use selected_video and selected_audio instead of best_video and best_audio
print("\n DOWNLOADING...")

vid_title = "vid"

# Download selected video and audio
print("\nDownloading selected video quality...")
video_file = selected_video.download(
    output_path=download_dir,
    filename=f"{vid_title}_video.{selected_video.subtype}"
)
print(f"Downloaded video: {os.path.basename(video_file)}")

print("Downloading selected audio quality...")
audio_file = selected_audio.download(
    output_path=download_dir,
    filename=f"{vid_title}_audio.{selected_audio.subtype}"
)
print(f"Downloaded audio: {os.path.basename(audio_file)}")



# Merge Video and Audio
# Check if FFmpeg is available
merged_file = os.path.join(download_dir, f"{vid_title}_merged.mp4")

print("\n--- MERGING ---")

merge_video_audio(video_file, audio_file, merged_file,path_ffmpeg)
print(f"Successfully merged files to: {os.path.basename(merged_file)}")
print("\nYou now have these files:")

print(f"1. {os.path.basename(merged_file)} - High quality merged file")
print(f"2. High-quality video: {video_file}")
print(f"3. Audio: {audio_file}")

# Rename and cleanup
if os.path.exists(merged_file):
    final_path = rename_and_cleanup(merged_file, video_file, audio_file, yt_file_name)
    if final_path:
        print(f"Final video saved as: {final_path}")
else:
    print("Merged file not found, cannot rename/cleanup")