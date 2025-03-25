import os
import subprocess
import shutil

def merge_video_audio(video_path, audio_path, output_path,path_ffmpeg):
    """Merge video and audio using FFmpeg with full path"""
    try:
        # Use the full path to FFmpeg
        cmd = f'"{path_ffmpeg}" -i "{video_path}" -i "{audio_path}" -c:v copy -c:a copy "{output_path}"'
        
        print(f"Running command:\n {cmd}")
        result = subprocess.run(
            cmd, 
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        if result.returncode != 0:
            print(f"Error output: {result.stderr[:200]}...")
            return False
            
        return True
    except Exception as e:
        print(f"Error during merge: {str(e)}")
        return False