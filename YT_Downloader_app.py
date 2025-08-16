# import yt_dlp
# import streamlit as st
# import requests
# from io import BytesIO

# def get_download_link(url, format_choice):
#     # Fix Shorts links
#     if "shorts" in url:
#         url = url.replace("shorts/", "watch?v=")

#     if format_choice.lower() == "mp4":
#         ydl_opts = {
#             "format": "best[ext=mp4][vcodec^=avc1]/best[ext=mp4]/best",
#             "noplaylist": True,
#             "quiet": True,
#         }
#         mime_type = "video/mp4"
#     elif format_choice.lower() == "mp3":
#         ydl_opts = {
#             "format": "bestaudio/best",
#             "noplaylist": True,
#             "quiet": True,
#             "postprocessors": [
#                 {
#                     "key": "FFmpegExtractAudio",
#                     "preferredcodec": "mp3",
#                     "preferredquality": "192",
#                 }
#             ],
#         }
#         mime_type = "audio/mpeg"
#     else:
#         return None, None, "Invalid format"

#     try:
#         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#             info = ydl.extract_info(url, download=False)  # ⬅ don’t download
#             download_url = info["url"]
#             title = info.get("title", "video")
#         return download_url, title, mime_type
#     except Exception as e:
#         return None, None, str(e)


# # --- Streamlit UI ---
# st.set_page_config(page_title="YouTube Video & Audio Downloader", layout="centered")
# st.title("YouTube Video & Audio Downloader")

# video_url = st.text_input("Enter the YouTube video URL:")
# format_choice = st.selectbox("Select the format:", ["mp4", "mp3"])

# if st.button("Download"):
#     if video_url:
#         with st.spinner("Preparing download..."):
#             link, title, mime = get_download_link(video_url, format_choice)
#             if link is None:
#                 st.error(f"An error occurred: {title}")  # title holds error message
#             else:
#                 st.success("Download ready!")

#                 # Preview if video
#                 if format_choice == "mp4":
#                     st.video(link)

#                 # Fetch into memory buffer for download_button
#                 response = requests.get(link, stream=True)
#                 buffer = BytesIO(response.content)

#                 st.download_button(
#                     label=f"Click here to download {format_choice.upper()}",
#                     data=buffer,
#                     file_name=f"{title}.{format_choice}",
#                     mime=mime,
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
