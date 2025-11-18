# import streamlit as st
# import yt_dlp
# import os
# import tempfile
# import re
# import time

# def sanitize_filename(filename):
#     """
#     Removes illegal characters from a string so it can be used as a
#     safe filename.
#     """
#     # Remove characters that are illegal in most filesystems
#     sanitized = re.sub(r'[\\/*?:"<>|]', "", filename)
#     # Replace whitespace with underscores
#     sanitized = re.sub(r'\s+', '_', sanitized)
#     # Limit length to avoid issues
#     return sanitized[:100]

# def get_video_info(url):
#     """
#     Uses yt-dlp to extract video information without downloading.
#     """
#     ydl_opts = {'noplaylist': True}
#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         try:
#             info = ydl.extract_info(url, download=False)
#             return info
#         except yt_dlp.utils.DownloadError as e:
#             st.error(f"Error extracting video info: {e}")
#             return None
#         except Exception as e:
#             st.error(f"An unexpected error occurred: {e}")
#             return None

# def run_downloader():
#     st.set_page_config(page_title="YouTube Downloader")
#     st.image("https://upload.wikimedia.org/wikipedia/commons/4/42/YouTube_icon_%282013-2017%29.png", width=100)
#     st.title("YouTube Video & Audio Downloader")
#     st.markdown("""
#     This application allows you to download videos from YouTube in various formats.
#     Simply enter the URL, select the desired format, and click download.
#     """)
#     st.markdown("Paste a YouTube video or short URL below to download it as MP4 or MP3.")

#     url = st.text_input("YouTube URL", placeholder="https.www.youtube.com/watch?v=...")
    
#     col1, col2 = st.columns(2)
#     with col1:
#         # format_choice = st.radio("Choose format", ("MP4 (Video)", "MP3 (Audio)"), key="format_choice")
#         format_choice = st.selectbox("Select the format:", ["MP4 (Video)", "MP3 (Audio)"], key="format_choice")
    
#     # We will show the download button only after processing
#     # Use session state to hold the download button data
#     if 'download_data' not in st.session_state:
#         st.session_state.download_data = None

#     if st.button("Process Video", key="process_button"):
#         st.session_state.download_data = None # Clear previous data
#         if not url:
#             st.warning("Please paste a URL first.")
#         else:
#             with st.spinner("Fetching video info..."):
#                 info = get_video_info(url)
            
#             if info:
#                 # Get title and sanitize it for the filename
#                 title = info.get('title', None)
                
#                 if format_choice == "MP4 (Video)":
#                     ext = "mp4"
#                     default_name = f"youtube_video.{ext}"
#                     mime_type = "video/mp4"
#                     ydl_opts = {
#                         'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
#                         'noplaylist': True,
#                         'postprocessors': [{
#                             'key': 'FFmpegVideoConvertor',
#                             'preferedformat': 'mp4',
#                         }],
#                     }
#                 else: # MP3 (Audio)
#                     ext = "mp3"
#                     default_name = f"youtube_audio.{ext}"
#                     mime_type = "audio/mpeg"
#                     ydl_opts = {
#                         'format': 'bestaudio/best',
#                         'noplaylist': True,
#                         'postprocessors': [{
#                             'key': 'FFmpegExtractAudio',
#                             'preferredcodec': 'mp3',
#                             'preferredquality': '192',
#                         }],
#                     }
                
#                 # Determine final filename
#                 if title:
#                     base_name = sanitize_filename(title)
#                     final_filename = f"{base_name}.{ext}"
#                 else:
#                     final_filename = default_name

#                 try:
#                     # Use a temporary directory to store the downloaded file
#                     with tempfile.TemporaryDirectory() as temp_dir:
#                         # Set the output template for yt-dlp
#                         # We give it an absolute path to the temp directory
#                         out_path = os.path.join(temp_dir, f"{base_name}_temp")
#                         ydl_opts['outtmpl'] = out_path

#                         with st.spinner(f"Downloading and converting to {ext}... This may take a moment."):
#                             # Start the download
#                             with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#                                 ydl.download([url])
                            
#                             # Find the resulting file (yt-dlp adds the .mp3/.mp4 extension)
#                             # The file will be named like 'video_title_temp.mp3'
#                             expected_file = f"{out_path}.{ext}"

#                             if os.path.exists(expected_file):
#                                 # Read the file into memory
#                                 with open(expected_file, 'rb') as f:
#                                     file_bytes = f.read()
                                
#                                 st.session_state.download_data = {
#                                     "bytes": file_bytes,
#                                     "filename": final_filename,
#                                     "mime": mime_type,
#                                     "title": info.get('title', 'Unknown Title')
#                                 }
#                                 st.success("Your file is ready!")
#                             else:
#                                 # Fallback search if the expected name isn't found
#                                 files_in_dir = os.listdir(temp_dir)
#                                 if files_in_dir:
#                                     actual_file = os.path.join(temp_dir, files_in_dir[0])
#                                     with open(actual_file, 'rb') as f:
#                                         file_bytes = f.read()
                                    
#                                     st.session_state.download_data = {
#                                         "bytes": file_bytes,
#                                         "filename": final_filename, # Still use the clean name
#                                         "mime": mime_type,
#                                         "title": info.get('title', 'Unknown Title')
#                                     }
#                                     st.success("Your file is ready!")
#                                 else:
#                                     st.error("Download failed. Could not find converted file.")
                
#                 except yt_dlp.utils.DownloadError as e:
#                     st.error(f"Download Error: {e}")
#                 except Exception as e:
#                     st.error(f"An unexpected error occurred during download: {e}")
#                     st.error("This often happens if FFmpeg is not installed or not in your system's PATH. See README.md for help.")

#     # If download data is in session state, show the download button
#     if st.session_state.download_data:
#         data = st.session_state.download_data
#         st.subheader(f"Download: {data['title']}")
#         st.download_button(
#             label=f"Click to Download {data['filename']}",
#             data=data['bytes'],
#             file_name=data['filename'],
#             mime=data['mime'],
#             on_click=lambda: st.session_state.clear() # Clear state after click
#         )

# if __name__ == "__main__":
#     run_downloader()



import streamlit as st
import yt_dlp
import os
import tempfile
import re

# --- CONFIGURATION ---
# specific the name of your cookie file here
COOKIE_FILE = 'cookies.txt' 

def sanitize_filename(filename):
    """
    Removes illegal characters from a string so it can be used as a
    safe filename.
    """
    sanitized = re.sub(r'[\\/*?:"<>|]', "", filename)
    sanitized = re.sub(r'\s+', '_', sanitized)
    return sanitized[:100]

def get_video_info(url):
    """
    Uses yt-dlp to extract video information without downloading.
    """
    ydl_opts = {
        'noplaylist': True,
        # FIX: Add cookiefile here so metadata extraction works
        'cookiefile': COOKIE_FILE if os.path.exists(COOKIE_FILE) else None
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            return info
        except yt_dlp.utils.DownloadError as e:
            st.error(f"Error extracting video info: {e}")
            return None
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
            return None

def run_downloader():
    st.set_page_config(page_title="YouTube Downloader")
    st.image("https://upload.wikimedia.org/wikipedia/commons/4/42/YouTube_icon_%282013-2017%29.png", width=100)
    st.title("YouTube Video & Audio Downloader")
    st.markdown("""
    This application allows you to download videos from YouTube in various formats.
    Simply enter the URL, select the desired format, and click download.
    """)
    
    # Warning if cookies.txt is missing
    if not os.path.exists(COOKIE_FILE):
        st.warning(f"⚠️ '{COOKIE_FILE}' not found. YouTube may block the download. Please export cookies.txt and place it in the app directory.")

    url = st.text_input("YouTube URL", placeholder="https://www.youtube.com/watch?v=...")
    
    col1, col2 = st.columns(2)
    with col1:
        format_choice = st.selectbox("Select the format:", ["MP4 (Video)", "MP3 (Audio)"], key="format_choice")
    
    if 'download_data' not in st.session_state:
        st.session_state.download_data = None

    if st.button("Process Video", key="process_button"):
        st.session_state.download_data = None 
        if not url:
            st.warning("Please paste a URL first.")
        else:
            with st.spinner("Fetching video info..."):
                info = get_video_info(url)
            
            if info:
                title = info.get('title', None)
                
                # Common options for both formats
                common_opts = {
                    'noplaylist': True,
                    # FIX: Add cookiefile here so the actual download works
                    'cookiefile': COOKIE_FILE if os.path.exists(COOKIE_FILE) else None,
                }

                if format_choice == "MP4 (Video)":
                    ext = "mp4"
                    default_name = f"youtube_video.{ext}"
                    mime_type = "video/mp4"
                    ydl_opts = {
                        **common_opts,
                        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                        'postprocessors': [{
                            'key': 'FFmpegVideoConvertor',
                            'preferedformat': 'mp4',
                        }],
                    }
                else: # MP3 (Audio)
                    ext = "mp3"
                    default_name = f"youtube_audio.{ext}"
                    mime_type = "audio/mpeg"
                    ydl_opts = {
                        **common_opts,
                        'format': 'bestaudio/best',
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                            'preferredquality': '192',
                        }],
                    }
                
                if title:
                    base_name = sanitize_filename(title)
                    final_filename = f"{base_name}.{ext}"
                else:
                    final_filename = default_name

                try:
                    with tempfile.TemporaryDirectory() as temp_dir:
                        out_path = os.path.join(temp_dir, f"{base_name}_temp")
                        ydl_opts['outtmpl'] = out_path

                        with st.spinner(f"Downloading and converting to {ext}..."):
                            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                                ydl.download([url])
                            
                            expected_file = f"{out_path}.{ext}"

                            if os.path.exists(expected_file):
                                with open(expected_file, 'rb') as f:
                                    file_bytes = f.read()
                                
                                st.session_state.download_data = {
                                    "bytes": file_bytes,
                                    "filename": final_filename,
                                    "mime": mime_type,
                                    "title": info.get('title', 'Unknown Title')
                                }
                                st.success("Your file is ready!")
                            else:
                                # Fallback search
                                files_in_dir = os.listdir(temp_dir)
                                if files_in_dir:
                                    actual_file = os.path.join(temp_dir, files_in_dir[0])
                                    with open(actual_file, 'rb') as f:
                                        file_bytes = f.read()
                                    
                                    st.session_state.download_data = {
                                        "bytes": file_bytes,
                                        "filename": final_filename, 
                                        "mime": mime_type,
                                        "title": info.get('title', 'Unknown Title')
                                    }
                                    st.success("Your file is ready!")
                                else:
                                    st.error("Download failed. Could not find converted file.")
                
                except yt_dlp.utils.DownloadError as e:
                    st.error(f"Download Error: {e}")
                except Exception as e:
                    st.error(f"An unexpected error occurred: {e}")

    if st.session_state.download_data:
        data = st.session_state.download_data
        st.subheader(f"Download: {data['title']}")
        st.download_button(
            label=f"Click to Download {data['filename']}",
            data=data['bytes'],
            file_name=data['filename'],
            mime=data['mime'],
            on_click=lambda: st.session_state.clear()
        )

if __name__ == "__main__":
    run_downloader()
