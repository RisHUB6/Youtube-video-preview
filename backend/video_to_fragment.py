from moviepy.editor import VideoFileClip
import os

def generate_snapshots(video_path, output_dir, rate=4):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    clip = VideoFileClip(video_path)
    duration = clip.duration
    fps = clip.fps

    # Calculate the time interval for snapshots
    interval = 1 / rate  # in seconds

    # Generate snapshots
    current_time = 0
    while current_time < duration:
        snapshot_path = os.path.join(output_dir, f'snapshot_{int(current_time * 1000):04d}.jpg')
        clip.save_frame(snapshot_path, current_time)
        current_time += interval

if __name__ == "__main__":
    video_path = 'video/video1.mp4'  # Change this to your video file path
    output_dir = 'video/video1_snapshots/'  # Change this to your output directory
    generate_snapshots(video_path, output_dir, rate=4)
