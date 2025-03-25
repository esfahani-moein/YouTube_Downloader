import os

def rename_and_cleanup(merged_file, video_file, audio_file, new_name):
    """
    Rename the merged file with a new name (keeping extension) and delete source files
    
    Args:
        merged_file: Path to the merged file
        video_file: Path to the video file to delete
        audio_file: Path to the audio file to delete
        new_name: New base filename (without extension)
    
    Returns:
        Path to the renamed file
    """
    try:
        # Make sure merged file exists
        if not os.path.exists(merged_file):
            print(f"Error: Merged file {merged_file} not found")
            return None
            
        # Get directory and extension from the merged file
        directory = os.path.dirname(merged_file)
        _, extension = os.path.splitext(merged_file)
        
        # Create new filename with original extension
        new_file_path = os.path.join(directory, f"{new_name}{extension}")
        
        # Rename the file
        os.rename(merged_file, new_file_path)
        print(f"Renamed merged file to: {os.path.basename(new_file_path)}")
        
        # Delete the source files
        if os.path.exists(video_file):
            os.remove(video_file)
            print(f"Deleted: {os.path.basename(video_file)}")
            
        if os.path.exists(audio_file):
            os.remove(audio_file)
            print(f"Deleted: {os.path.basename(audio_file)}")
            
        return new_file_path
    except Exception as e:
        print(f"Error during rename/cleanup: {str(e)}")
        return None