# import os
# import streamlit as st

# ffmpeg_path = os.popen('which ffmpeg').read().strip()
# st.write("FFmpeg Path:", ffmpeg_path)


import streamlit as st
import yt_dlp
import re

# Validate YouTube URL
def is_valid_youtube_url(url):
    youtube_regex = (
        r'(https?://)?(www\.)?'
        r'(youtube|youtu|youtube-nocookie)\.(com|be)/'
        r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
    return re.match(youtube_regex, url)

# Fetch video information
def get_video_info(url):
    try:
        ydl_opts = {'quiet': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get('title')
            description = info.get('description')
            thumbnail = info.get('thumbnail')
            # Limit description to 20 words
            if description:
                description = ' '.join(description.split()[:20]) + '...'
            return title, description, thumbnail
    except Exception:
        return None, None, None

# Download video
def download_video(url, format_choice):
    # Configure options for yt-dlp
    ydl_opts = {
        'outtmpl': '%(title)s.%(ext)s',  # Output file name format
        'ffmpeg_location': ' /usr/bin/ffmpeg',  # Path to FFmpeg, adjust if needed
    }

    # Set format based on user choice
    if format_choice.lower() == 'mp4':
            ydl_opts = {
    'format': 'bestvideo+bestaudio/best',
    'merge_output_format': 'mp4',
    'ffmpeg_location': '/usr/bin/ffmpeg',  # Path to FFmpeg
    'outtmpl': '%(title)s.%(ext)s',
}

        
    elif format_choice.lower() == 'mp3':
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        })
    else:
        return "Invalid format choice. Please choose 'mp4' or 'mp3'."

    # Download the video/audio
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            info_dict = ydl.extract_info(url, download=False)
            title = info_dict.get('title', None)
            return f"Download completed successfully: {title}"
    except Exception as e:
        return f"An error occurred: {e}"


# Streamlit UI
st.set_page_config(page_title="YouTube Video & Audio Downloader", layout="centered")
st.image("https://upload.wikimedia.org/wikipedia/commons/4/42/YouTube_icon_%282013-2017%29.png", width=100)
st.title("YouTube Video Downloader")

st.markdown("""
This application allows you to download videos from YouTube in various formats. 
Simply enter the URL of the video you want to download, select the desired format, 
and click the download button. Enjoy your favorite content offline!
""")

# Initialize session state for video info
if "video_info" not in st.session_state:
    st.session_state.video_info = {"title": None, "description": None, "thumbnail": None}

# Input and fetch video info
video_url = st.text_input("Enter the YouTube video URL:", key="video_url_input")
if video_url and is_valid_youtube_url(video_url):
    if st.button("Fetch Video Info"):
        title, description, thumbnail = get_video_info(video_url)
        st.session_state.video_info = {"title": title, "description": description, "thumbnail": thumbnail}

# Display video info
if st.session_state.video_info["thumbnail"]:
    st.image(st.session_state.video_info["thumbnail"], caption="Video Thumbnail", width=500)
if st.session_state.video_info["title"]:
    st.markdown(f"**Title:** {st.session_state.video_info['title']}")
if st.session_state.video_info["description"]:
    st.markdown(f"**Description:** {st.session_state.video_info['description']}")

# Format selection and download
format_choice = st.selectbox("Select the format:", ["mp4", "mp3"], key="format_choice")

if st.button("Download"):
    if video_url and is_valid_youtube_url(video_url):
        with st.spinner("Downloading..."):
            result = download_video(video_url, format_choice)
            st.success(result)
    else:
        st.error("Invalid YouTube URL. Please enter a valid link.")
