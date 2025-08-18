# import yt_dlp
# import streamlit as st
# import re
# import os

# # --- Download function (Updated to use cookies) ---
# def download_video_data(url, format_choice):
#     if "shorts" in url:
#         url = url.replace("shorts/", "watch?v=")
    
#     # The temporary file where the video will be downloaded
#     temp_filename = f"temp_download.{format_choice}"
    
#     ydl_opts = {
#         'noplaylist': True,
#         'outtmpl': temp_filename,
#         # --- KEY CHANGE: Use the cookies file to bypass 403 errors ---
#         'cookiefile': 'cookies.txt', 
#     }

#     if format_choice == 'mp4':
#         ydl_opts['format'] = 'best[ext=mp4][vcodec^=avc1]/best[ext=mp4]/best'
#     elif format_choice == 'mp3':
#         ydl_opts['format'] = 'bestaudio/best'
#         ydl_opts['postprocessors'] = [{
#             'key': 'FFmpegExtractAudio',
#             'preferredcodec': 'mp3',
#             'preferredquality': '192',
#         }]

#     try:
#         # Check if cookies.txt exists before trying to download
#         if not os.path.exists('cookies.txt'):
#             return None, None, "Error: cookies.txt file not found. Please add it to the project folder."

#         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#             info = ydl.extract_info(url, download=True)
#             title = info.get('title', 'video')

#         # Read the downloaded file into memory
#         with open(temp_filename, 'rb') as f:
#             data = f.read()
        
#         # Clean up the temporary file
#         os.remove(temp_filename)
        
#         return data, title, None

#     except Exception as e:
#         # Clean up the temp file if it exists, even after an error
#         if os.path.exists(temp_filename):
#             os.remove(temp_filename)
#         return None, None, str(e)


# # --- Streamlit UI (No changes needed here) ---
# st.set_page_config(page_title="YouTube Video & Audio Downloader", layout="centered")
# st.image("https://upload.wikimedia.org/wikipedia/commons/4/42/YouTube_icon_%282013-2017%29.png", width=100)
# st.title("YouTube Video & Audio Downloader")

# st.markdown("""
# This application allows you to download videos from YouTube in various formats.
# Simply enter the URL, select the desired format, and click download.
# """)

# video_url = st.text_input("Enter the YouTube video URL:")
# format_choice = st.selectbox("Select the format:", ["mp4", "mp3"])

# if st.button("Download"):
#     if video_url:
#         with st.spinner(f"Downloading {format_choice.upper()}... Please wait."):
#             video_data, title, error = download_video_data(video_url, format_choice)

#             if error:
#                 st.error(f"An error occurred: {error}")
#             else:
#                 st.success("Download ready!")
#                 safe_filename = re.sub(r'[\\/*?:"<>|]', "", title)
#                 full_filename = f"{safe_filename}.{format_choice.lower()}"
                
#                 st.download_button(
#                    label=f"Click to download {full_filename}",
#                    data=video_data,
#                    file_name=full_filename,
#                    mime=f"audio/mpeg" if format_choice == 'mp3' else "video/mp4"
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

