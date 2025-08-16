


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


import os
import yt_dlp
import streamlit as st
import subprocess
import re

# --- Safe filename function ---
def safe_filename(text, max_length=80):
    text = re.sub(r'[\\/*?:"<>|]', "", text)  # remove invalid chars
    text = text.strip().replace(" ", "_")
    return text[:max_length]

# --- Download function ---
def download_video(url, format_choice):
    # Fix Shorts links
    if "shorts" in url:
        url = url.replace("shorts/", "watch?v=")

    download_folder = "downloads/"
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    if format_choice.lower() == "mp4":
        ydl_opts = {
            "format": "bestvideo+bestaudio/best",
            "merge_output_format": "mp4",
            "outtmpl": os.path.join(download_folder, "%(id)s.%(ext)s"),
            "quiet": True,
        }
        ext = "mp4"
    elif format_choice.lower() == "mp3":
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": os.path.join(download_folder, "%(id)s.%(ext)s"),
            "quiet": True,
        }
        ext = "mp3"
    else:
        return None, "Invalid format"

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            description = info.get("description", "video")
            filename_base = safe_filename(description)
            downloaded_file = ydl.prepare_filename(info)

            # Final renamed file
            final_file = os.path.join(download_folder, f"{filename_base}.{ext}")

            # If MP3 and downloaded as .webm, convert
            if downloaded_file.endswith(".webm") and format_choice == "mp3":
                subprocess.run(
                    ["ffmpeg", "-i", downloaded_file, final_file],
                    check=True
                )
                os.remove(downloaded_file)
            else:
                os.rename(downloaded_file, final_file)

        return final_file, None
    except Exception as e:
        return None, str(e)


# --- Streamlit UI ---
st.set_page_config(page_title="YouTube Video & Audio Downloader", layout="centered")
st.image("https://upload.wikimedia.org/wikipedia/commons/4/42/YouTube_icon_%282013-2017%29.png", width=100)
st.title("YouTube Video & Audio Downloader")

st.markdown("""
This application allows you to download videos from YouTube in **MP4 or MP3** format.  
The downloaded file will be saved with the **video description** as filename.
""")

video_url = st.text_input("Enter the YouTube video URL:")
format_choice = st.selectbox("Select the format:", ["mp4", "mp3"])

if st.button("Download"):
    if video_url:
        with st.spinner("Downloading..."):
            file_path, error = download_video(video_url, format_choice)
            if error:
                st.error(f"❌ Error: {error}")
            else:
                st.success("✅ Download ready!")

                if format_choice == "mp4":
                    st.video(file_path)  # preview video

                # Provide download button
                with open(file_path, "rb") as file:
                    st.download_button(
                        label=f"⬇️ Download {format_choice.upper()}",
                        data=file,
                        file_name=os.path.basename(file_path),
                        mime="video/mp4" if format_choice == "mp4" else "audio/mpeg",
                    )
    else:
        st.error("Please enter a valid YouTube URL.")
