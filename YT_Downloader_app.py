# import yt_dlp
# import streamlit as st
# from io import BytesIO
# import os

# # --- Download function ---
# def download_video(url, format_choice):
#     # Fix Shorts links
#     if "shorts" in url:
#         url = url.replace("shorts/", "watch?v=")

#     buffer = BytesIO()

#     if format_choice.lower() == "mp4":
#         ydl_opts = {
#             "format": "best[ext=mp4][vcodec^=avc1]/best[ext=mp4]/best",
#             "merge_output_format": "mp4",
#             "noplaylist": True,
#             "quiet": True,
#             "outtmpl": "-",  # stream to stdout
#         }
#     elif format_choice.lower() == "mp3":
#         ydl_opts = {
#             "format": "bestaudio/best",
#             "noplaylist": True,
#             "quiet": True,
#             "outtmpl": "-", 
#             "postprocessors": [
#                 {
#                     "key": "FFmpegExtractAudio",
#                     "preferredcodec": "mp3",
#                     "preferredquality": "192",
#                 }
#             ],
#         }
#     else:
#         return None, None, "Invalid format"

#     try:
#         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#             info = ydl.extract_info(url, download=False)
#             filename = ydl.prepare_filename(info)

#             # Download into file
#             ydl.download([url])

#         return filename, info.get("title", "video"), None
#     except Exception as e:
#         return None, None, str(e)


# # --- Streamlit UI ---
# st.set_page_config(page_title="YouTube Video & Audio Downloader", layout="centered")
# st.image("https://upload.wikimedia.org/wikipedia/commons/4/42/YouTube_icon_%282013-2017%29.png", width=100)
# st.title("YouTube Video & Audio Downloader")

# st.markdown("""
# This app lets you download YouTube videos in MP4 or MP3 format.  
# Paste a link, choose format, and download.
# """)

# video_url = st.text_input("Enter YouTube video URL:")
# format_choice = st.selectbox("Select format:", ["mp4", "mp3"])

# if st.button("Download"):
#     if video_url:
#         with st.spinner("Downloading..."):
#             file_path, title, error = download_video(video_url, format_choice)
#             if error:
#                 st.error(f"❌ Error: {error}")
#             else:
#                 st.success(f"✅ {title} downloaded!")

#                 # Read file into memory
#                 with open(file_path, "rb") as f:
#                     file_bytes = f.read()

#                 st.download_button(
#                     label=f"⬇️ Download {format_choice.upper()}",
#                     data=file_bytes,
#                     file_name=os.path.basename(file_path),
#                     mime="video/mp4" if format_choice == "mp4" else "audio/mp3",
#                 )
#     else:
#         st.error("Please enter a valid YouTube URL.")




import yt_dlp
import streamlit as st
from io import BytesIO
import subprocess
import os

# --- Download function ---
def download_video(url, format_choice):
    # Fix Shorts links
    if "shorts" in url:
        url = url.replace("shorts/", "watch?v=")

    buffer = BytesIO()

    if format_choice.lower() == "mp4":
        ydl_opts = {
            "format": "best[ext=mp4][vcodec^=avc1]/best[ext=mp4]/best",
            "merge_output_format": "mp4",
            "noplaylist": True,
            "outtmpl": "-",  # output to stdout (memory)
            "quiet": True,
            "http_headers": {"User-Agent": "Mozilla/5.0"},
        }
    elif format_choice.lower() == "mp3":
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": "-", 
            "quiet": True,
            "noplaylist": True,
            "postprocessors": [
                {  # Extract audio using ffmpeg
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
            "http_headers": {"User-Agent": "Mozilla/5.0"},
        }
    else:
        return None, "Invalid format"

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            # Get direct media URL instead of downloading
            download_url = info["url"]
            return download_url, None
    except Exception as e:
        return None, str(e)


# --- Streamlit UI ---
st.set_page_config(page_title="YouTube Video & Audio Downloader", layout="centered")
st.image("https://upload.wikimedia.org/wikipedia/commons/4/42/YouTube_icon_%282013-2017%29.png", width=100)
st.title("YouTube Video & Audio Downloader")

st.markdown("""
This application allows you to download videos from YouTube in various formats.  
Simply enter the URL, select the desired format, and click download.
""")

video_url = st.text_input("Enter the YouTube video URL:")
format_choice = st.selectbox("Select the format:", ["mp4", "mp3"])

if st.button("Download"):
    if video_url:
        with st.spinner("Fetching download link..."):
            download_url, error = download_video(video_url, format_choice)
            if error:
                st.error(f"An error occurred: {error}")
            else:
                st.success("Download ready!")
                if format_choice == "mp4":
                    st.video(download_url)  # preview
                st.markdown(f"[Click here to download {format_choice.upper()}]({download_url})")
    
                
                
    else:
        st.error("Please enter a valid YouTube URL.")
