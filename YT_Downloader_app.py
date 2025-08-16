


# import yt_dlp
# import streamlit as st
# from io import BytesIO
# import subprocess
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
#             "outtmpl": "-",  # output to stdout (memory)
#             "quiet": True,
#             "http_headers": {"User-Agent": "Mozilla/5.0"},
#         }
#     elif format_choice.lower() == "mp3":
#         ydl_opts = {
#             "format": "bestaudio/best",
#             "outtmpl": "-", 
#             "quiet": True,
#             "noplaylist": True,
#             "postprocessors": [
#                 {  # Extract audio using ffmpeg
#                     "key": "FFmpegExtractAudio",
#                     "preferredcodec": "mp3",
#                     "preferredquality": "192",
#                 }
#             ],
#             "http_headers": {"User-Agent": "Mozilla/5.0"},
#         }
#     else:
#         return None, "Invalid format"

#     try:
#         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#             info = ydl.extract_info(url, download=False)
#             # Get direct media URL instead of downloading
#             download_url = info["url"]
#             return download_url, None
#     except Exception as e:
#         return None, str(e)


# # --- Streamlit UI ---
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
#         with st.spinner("Fetching download link..."):
#             download_url, error = download_video(video_url, format_choice)
#             if error:
#                 st.error(f"An error occurred: {error}")
#             else:
#                 st.success("Download ready!")
#                 if format_choice == "mp4":
#                     st.video(download_url)  # preview
#                 st.markdown(f"[Click here to download {format_choice.upper()}]({download_url})")
    
                
                
#     else:
#         st.error("Please enter a valid YouTube URL.")


import yt_dlp
import streamlit as st
from io import BytesIO
import os

# --- Download function ---
def download_video(url, format_choice):
    try:
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "format": "bestvideo+bestaudio/best" if format_choice == "mp4" else "bestaudio/best",
            "merge_output_format": format_choice,
            "noplaylist": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            # ✅ Use video description as filename
            video_description = info.get("description", "video").split("\n")[0][:50]  
            # take first line, max 50 chars
            safe_filename = "".join(c for c in video_description if c.isalnum() or c in " _-").rstrip()
            filename = f"{safe_filename}.{format_choice}"

            buffer = BytesIO()
            ydl.download([url])

            # Save downloaded file temporarily
            if os.path.exists(info["title"] + f".{format_choice}"):
                os.rename(info["title"] + f".{format_choice}", filename)

            return filename, info

    except Exception as e:
        return None, str(e)

# --- Streamlit UI ---
st.title("🎥 YouTube Downloader")

url = st.text_input("Enter YouTube Video URL:")
format_choice = st.selectbox("Choose format:", ["mp4", "mp3"])

if st.button("Download"):
    if url:
        with st.spinner("Downloading..."):
            filename, info = download_video(url, format_choice)

            if filename:
                st.success("Download complete!")

                with open(filename, "rb") as f:
                    st.download_button(
                        label="📥 Download File",
                        data=f,
                        file_name=filename,
                        mime="video/mp4" if format_choice == "mp4" else "audio/mpeg"
                    )
            else:
                st.error(f"❌ Error: {info}")
    else:
        st.warning("Please enter a YouTube URL.")
