# import os
# import yt_dlp
# import streamlit as st

# # Define the download function
# def download_video(url, format_choice):
#     if format_choice.lower() == 'mp4':
#         ydl_opts = {
#             'format': 'bestvideo+bestaudio/best',
#             'merge_output_format': 'mp4',
#             'ffmpeg_location': '/usr/bin/ffmpeg',  # Path to FFmpeg
#             'outtmpl': 'downloads/%(title)s.%(ext)s',  # Save to 'downloads' folder
#         }
#     elif format_choice.lower() == 'mp3':
#         ydl_opts = {
#             'format': 'bestaudio/best',
#             'postprocessors': [{
#                 'key': 'FFmpegExtractAudio',
#                 'preferredcodec': 'mp3',
#                 'preferredquality': '192',
#             }],
#             'outtmpl': 'downloads/%(title)s.%(ext)s',  # Save to 'downloads' folder
#         }
#     else:
#         return "Invalid format choice. Please choose 'mp4' or 'mp3'."

#     try:
#         # Download video
#         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#             info_dict = ydl.extract_info(url, download=True)
#             filename = ydl.prepare_filename(info_dict)
#             return filename  # Return the saved filename
#     except Exception as e:
#         return f"An error occurred: {e}"

# # Streamlit UI
# st.set_page_config(page_title="YouTube Video & Audio Downloader", layout="centered")
# st.title("YouTube Video Downloader")

# # Input and fetch video URL
# video_url = st.text_input("Enter the YouTube video URL:")
# format_choice = st.selectbox("Select the format:", ["mp4", "mp3"])

# if st.button("Download"):
#     if video_url:
#         with st.spinner("Downloading..."):
#             result = download_video(video_url, format_choice)
#             if result.startswith("An error occurred"):
#                 st.error(result)
#             else:
#                 st.success(f"Download completed successfully: {result}")

#                 # Provide a download button for the user to download the file
#                 with open(result, "rb") as file:
#                     st.download_button(
#                         label="Download Video",
#                         data=file,
#                         file_name=os.path.basename(result),
#                         mime="video/mp4" if format_choice == 'mp4' else "audio/mpeg"
#                     )
#     else:
#         st.error("Please enter a valid YouTube URL.")

import os
import yt_dlp
import streamlit as st

# Define the download function
def download_video(url, format_choice):
    download_folder = 'downloads/'
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)  # Create the folder if it doesn't exist

    if format_choice.lower() == 'mp4':
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4',
            'ffmpeg_location': '/usr/bin/ffmpeg',  # Path to FFmpeg
            'outtmpl': os.path.join(download_folder, '%(title)s.%(ext)s'),  # Save to 'downloads' folder
        }
    elif format_choice.lower() == 'mp3':
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': os.path.join(download_folder, '%(title)s.%(ext)s'),  # Save to 'downloads' folder
        }
    else:
        return "Invalid format choice. Please choose 'mp4' or 'mp3'."

    try:
        # Download video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info_dict)
            return filename  # Return the saved filename
    except Exception as e:
        return f"An error occurred: {e}"

# Streamlit UI
st.set_page_config(page_title="YouTube Video & Audio Downloader", layout="centered")
st.title("YouTube Video Downloader")

# Input and fetch video URL
video_url = st.text_input("Enter the YouTube video URL:")
format_choice = st.selectbox("Select the format:", ["mp4", "mp3"])

# Button for downloading and providing the download link
if st.button("Download Video"):
    if video_url:
        with st.spinner("Downloading..."):
            result = download_video(video_url, format_choice)
            if result.startswith("An error occurred"):
                st.error(result)
            else:
                st.success(f"Download completed successfully: {result}")

                # Provide a download button for the user to download the file
                file_path = os.path.join('downloads', os.path.basename(result))

                if os.path.exists(file_path):
                    with open(file_path, "rb") as file:
                        st.download_button(
                            label="Click to Download Video",
                            data=file,
                            file_name=os.path.basename(result),
                            mime="video/mp4" if format_choice == 'mp4' else "audio/mpeg"
                        )
                else:
                    st.error("File not found.")
    else:
        st.error("Please enter a valid YouTube URL.")


