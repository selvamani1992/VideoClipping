import streamlit as st
from moviepy.editor import VideoFileClip
import os
from io import BytesIO
import zipfile

st.set_page_config(page_title="Video Splitter",
                   page_icon="",
                   layout="wide",
                   initial_sidebar_state="expanded")

def split_and_save_video(video_file, time_frame):
    # Get the file extension
    file_extension = video_file.name.split('.')[-1]

    # Create a temporary file to save the uploaded video
    temp_video_path = f"temp_video.{file_extension}"
    with open(temp_video_path, "wb") as temp_file:
        temp_file.write(video_file.read())

    # Create VideoFileClip and close it explicitly after using it
    clip = VideoFileClip(temp_video_path)
    duration = clip.duration
    num_clips = int(duration / time_frame)
    clips = [clip.subclip(i * time_frame, (i + 1) * time_frame) for i in range(num_clips)]

    # Save video clips locally and provide download links
    download_links = []
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for i, video_clip in enumerate(clips):
            output_path = f"output_clip_{i + 1}.mp4"
            video_clip.write_videofile(output_path)
            download_links.append(output_path)
            zip_file.write(output_path)

    zip_buffer.seek(0)
    clip.close()
    # Delete the temporary video file
    os.remove(temp_video_path)

    return zip_buffer


def main():
    st.title("Video Splitter")
    st.markdown("<p style='color: white;'><b>This Streamlit app allows users to upload a video file and split it into "
                "smaller clips based on a specified time frame. Users can input the time frame in seconds and click "
                "the 'Split Video' button. The app then processes the uploaded video, splits it into segments, "
                "saves the segments as individual video files, and compresses them into a ZIP archive. "
                "Users can download all the split video clips at once by clicking the 'Download All Clips button'. "
                "</b></p><br>",unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload a video file", type=["mp4"])
    time_frame = st.number_input("Time Frame (in seconds)", min_value=1, value=3)
    if st.button("Split Video"):
        if uploaded_file is not None:
            zip_buffer = split_and_save_video(uploaded_file, time_frame)
            st.success("Video has been split. Click below to download all clips.")
            st.download_button(
                label="Download All Clips",
                data=zip_buffer,
                file_name='video_clips.zip',
                mime='application/zip'
            )
        else:
            st.error("Please upload a video file.")

if __name__ == "__main__":
    main()