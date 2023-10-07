import streamlit as st
from moviepy.editor import VideoFileClip
import os


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
    for i, video_clip in enumerate(clips):
        output_path = f"output_clip_{i + 1}.mp4"
        video_clip.write_videofile(output_path)
        download_links.append(output_path)

        # Display download link for each segment
        st.success(f"Segment {i + 1} has been split. [Download {output_path}](sandbox:/{output_path})")

    # Close the VideoFileClip object
    clip.close()

    # Delete the temporary video file
    os.remove(temp_video_path)

    return download_links


def main():
    st.title("Video Splitter")
    uploaded_file = st.file_uploader("Upload a video file", type=["mp4"])
    time_frame = st.number_input("Time Frame (in seconds)", min_value=1, value=3)
    if st.button("Split Video"):
        if uploaded_file is not None:
            split_and_save_video(uploaded_file, time_frame)
        else:
            st.error("Please upload a video file.")


if __name__ == "__main__":
    main()