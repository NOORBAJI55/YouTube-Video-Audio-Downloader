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

# --- Download function ---
def download_video(url, format_choice):
    # Fix Shorts links
    if "shorts" in url:
        url = url.replace("shorts/", "watch?v=")

    # Temporary file buffer
    buffer = BytesIO()

    if format_choice.lower() == "mp4":
        ydl_opts = {
            "format": "best[ext=mp4][vcodec^=avc1]/best[ext=mp4]/best",
            "merge_output_format": "mp4",
            "noplaylist": True,
            "outtmpl": "-",  # write to stdout (in-memory)
            "quiet": True,
        }
        mime_type = "video/mp4"

    elif format_choice.lower() == "mp3":
        ydl_opts = {
            "format": "bestaudio/best",
            "noplaylist": True,
            "outtmpl": "-", 
            "quiet": True,
            "postprocessors": [
                {  # Extract audio
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
        }
        mime_type = "audio/mpeg"
    else:
        return None, None, "Invalid format"

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        # Load downloaded file into buffer
        with open(filename, "rb") as f:
            buffer.write(f.read())
        buffer.seek(0)

        return buffer, filename, mime_type
    except Exception as e:
        return None, None, str(e)


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
        with st.spinner("Downloading... Please wait"):
            buffer, filename, result = download_video(video_url, format_choice)
            if buffer is None:
                st.error(f"An error occurred: {result}")
            else:
                st.success("Download ready!")
                # Preview if video
                if format_choice == "mp4":
                    st.video(buffer)

                # Actual download button
                st.download_button(
                    label=f"Click here to download {format_choice.upper()}",
                    data=buffer,
                    file_name=filename.split("/")[-1],
                    mime=result if isinstance(result, str) else result,
                )
    else:
        st.error("Please enter a valid YouTube URL.")
