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




import streamlit as st
import yt_dlp
import os

st.title("📥 YouTube Video & Audio Downloader")

url = st.text_input("Enter YouTube URL:")
download_btn = st.button("Click here to download MP4")

if download_btn and url:
    try:
        ydl_opts = {
            "format": "bestvideo+bestaudio/best",
            "merge_output_format": "mp4",  # force MP4 merge
            "outtmpl": "downloaded.%(ext)s",  # fixed output filename
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            st.write("⬇️ Downloading...")
            ydl.download([url])

        # After download, serve the file
        if os.path.exists("downloaded.mp4"):
            with open("downloaded.mp4", "rb") as f:
                st.download_button(
                    label="🎬 Save Video",
                    data=f,
                    file_name="video.mp4",
                    mime="video/mp4"
                )
            os.remove("downloaded.mp4")  # cleanup after download
        else:
            st.error("Download failed — file not found.")

    except Exception as e:
        st.error(f"An error occurred: {e}")
