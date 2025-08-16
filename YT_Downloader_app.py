import yt_dlp
import streamlit as st
import re
from io import BytesIO # Important for handling the file in memory

# --- Download function (Updated to download data into memory) ---
def download_video(url, format_choice):
    # Fix Shorts links
    if "shorts" in url:
        url = url.replace("shorts/", "watch?v=")
    
    # This buffer will hold the downloaded file data in memory
    buffer = BytesIO()

    if format_choice.lower() == "mp4":
        ydl_opts = {
            "format": "best[ext=mp4][vcodec^=avc1]/best[ext=mp4]/best",
            "outtmpl": "-",  # This is crucial: it tells yt-dlp to output to stdout
            "logtostderr": True, # Required when outputting to stdout
            "noplaylist": True,
            "http_headers": {"User-Agent": "Mozilla/5.0"},
        }
    elif format_choice.lower() == "mp3":
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": "-", # Output to stdout
            "logtostderr": True,
            "noplaylist": True,
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
            "http_headers": {"User-Agent": "Mozilla/5.0"},
        }
    else:
        return None, None, "Invalid format"

    try:
        # Redirect stdout to our memory buffer
        ydl_opts['outtmpl'] = {'default': 'pipe:1'}
        ydl_opts['progress_hooks'] = [lambda d: buffer.write(d['fragment_data']) if d['status'] == 'downloading' else None]

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
             info = ydl.extract_info(url, download=True)
             title = info.get('title', 'video')
             # Download happens via the hook, now we get the buffer's content
             # Since hooks handle writing, let's try a simpler stdout redirection
    
    # A more reliable method for Streamlit Cloud is to download to a temp file
    # But for local use, downloading to memory is cleaner. Let's correct the memory part.
    
    except Exception as e:
        # Let's try a different, more stable method for capturing output
        try:
            # Re-initialize buffer for a clean slate
            buffer = BytesIO()
            
            # Simplified opts for direct download to buffer
            if format_choice.lower() == "mp3":
                 ydl_opts['postprocessors'][0]['outtmpl'] = '-' # Ensure postprocessor outputs to stdout
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False) # Get info first
                title = info.get('title', 'video')
                
                # Now perform the actual download to the buffer
                # This part is complex; a simpler approach is needed for Streamlit.
                # The most reliable way is often to save to a file and read it.
                # Let's pivot to the most robust solution.
                
                # --- The correct and simplest approach for memory download ---
                ydl_opts['outtmpl'] = '-' # Output to stdout
                ydl_opts['logtostderr'] = True
                
                # We need to capture the output from the process
                proc = yt_dlp.YoutubeDL(ydl_opts).download([url])
                # This doesn't return data directly. The stdout method is complex.
                
                # Let's stick to the simplest working model: download to file, then serve.
                # This is more resource-intensive but foolproof.
                
                # Final working approach for robust memory download:
                data_buffer = BytesIO()
                ydl_opts['outtmpl'] = 'pipe:1'
                ydl_opts['fileobject'] = data_buffer

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    title = info.get('title', 'video')
                
                return data_buffer.getvalue(), title, None

        except Exception as e_final:
            return None, None, str(e_final)

# A more simplified and correct download function
def download_video_data(url, format_choice):
    if "shorts" in url:
        url = url.replace("shorts/", "watch?v=")
    
    # Temporary filename to save the download
    temp_filename = f"temp_download.{format_choice}"
    
    ydl_opts = {
        'noplaylist': True,
        'outtmpl': temp_filename,
        'http_headers': {"User-Agent": "Mozilla/5.0"},
    }

    if format_choice == 'mp4':
        ydl_opts['format'] = 'best[ext=mp4][vcodec^=avc1]/best[ext=mp4]/best'
    elif format_choice == 'mp3':
        ydl_opts['format'] = 'bestaudio/best'
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get('title', 'video')

        # Read the downloaded file into memory
        with open(temp_filename, 'rb') as f:
            data = f.read()
        
        # Clean up the temporary file
        import os
        os.remove(temp_filename)
        
        return data, title, None

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

# Using a placeholder to show the button after the link is ready
placeholder = st.empty()

if st.button("Download"):
    if video_url:
        with st.spinner(f"Downloading {format_choice.upper()}... Please wait."):
            # Use the new function that returns raw data
            video_data, title, error = download_video_data(video_url, format_choice)

            if error:
                st.error(f"An error occurred: {error}")
            else:
                st.success("Download ready!")

                # Sanitize the title to create a valid filename
                safe_filename = re.sub(r'[\\/*?:"<>|]', "", title)
                full_filename = f"{safe_filename}.{format_choice.lower()}"
                
                # --- CHANGE IS HERE ---
                # Use st.download_button instead of st.markdown
                st.download_button(
                   label=f"Click to download {full_filename}",
                   data=video_data,
                   file_name=full_filename,
                   mime=f"audio/mpeg" if format_choice == 'mp3' else "video/mp4"
                )
    else:
        st.error("Please enter a valid YouTube URL.")


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

