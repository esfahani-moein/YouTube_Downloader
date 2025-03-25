# YouTube_Downloader
A simple easy to use High Quality YouTube Downloader in Python
# YouTube Downloader

A Python utility for downloading high-quality YouTube videos with separate video and audio streams, then merging them into a single file.

## Features

- Download YouTube videos in the highest available quality
- Supports both combined and separate video/audio streams
- Interactive command-line interface for quality selection
- Automatic merging of separate video and audio streams using FFmpeg
- Clean file management with automatic cleanup

## Requirements

- Python 3.6+
- FFmpeg installed on your system
- Required Python packages (see requirements.txt)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/YouTube_Downloader.git
   cd YouTube_Downloader
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Install FFmpeg:
   - Windows: Download from [ffmpeg.org](https://ffmpeg.org/download.html) and update the `path_ffmpeg` variable in the script
   - macOS: `brew install ffmpeg`
   - Linux: `sudo apt install ffmpeg` (Ubuntu/Debian) or equivalent for your distribution

## Usage

1. Edit the script to specify your YouTube URL and download directory:
   ```python
   url = "your YouTube URL here"
   download_dir = r"your download directory path here"
   ```

2. Run the script:
   ```
   python project_ytdownloader.py
   ```

3. Follow the interactive prompts to select video and audio quality.

4. The script will download both streams and merge them into a high-quality MP4 file.

## How It Works

1. The script fetches all available stream information from YouTube
2. It displays progressive streams (combined video/audio) and separate high-quality video streams
3. You select your preferred video and audio quality
4. The script downloads both streams separately
5. FFmpeg merges them into a single high-quality MP4 file
6. The temporary files are cleaned up, leaving only the final merged video

## Project Structure

- project_ytdownloader.py: Main script
- utils: Helper modules
  - `request_patch.py`: Fixes for YouTube API requests
  - `file_info.py`: File naming and metadata utilities
  - `video_merge.py`: FFmpeg integration for merging streams
  - `cleanup.py`: File management and cleanup operations

## License

MIT


## Disclaimer

This tool is for personal use and learning python coding only. Please respect YouTube's terms of service and copyright laws.