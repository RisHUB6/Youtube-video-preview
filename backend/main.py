from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
import redis
import os
import base64
from typing import List
from moviepy.editor import VideoFileClip
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to the specific origin if you want to restrict
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Redis client
r = redis.Redis(host='localhost', port=6379, db=0)

# Path to the video file
VIDEO_PATH = '/Users/macbook/Desktop/video_preview/backend/video/video1.mp4'
SNAPSHOT_DIR = '/Users/macbook/Desktop/video_preview/backend/video/video1_snapshots'

class SnapshotsResponse(BaseModel):
    snapshots: List[str]

def generate_snapshots(video_path, output_dir, rate=4):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    clip = VideoFileClip(video_path)
    duration = clip.duration
    fps = clip.fps
    
    # Calculate the time interval for snapshots
    interval = max(1, int(fps / rate))
    
    snapshot_paths = []
    for t in range(0, int(duration * rate)):
        snapshot_path = os.path.join(output_dir, f'snapshot_{t:04d}.jpg')
        clip.save_frame(snapshot_path, t / rate)
        snapshot_paths.append(snapshot_path)
    
    return snapshot_paths

@app.get("/api/videos/snapshots", response_model=SnapshotsResponse)
async def get_snapshots():
    if r.get("snapshot"):
        snapshot_paths = r.get("snapshot").decode().split(",")
    else:
        snapshot_paths = generate_snapshots(VIDEO_PATH, SNAPSHOT_DIR)
        r.set("snapshot", ",".join(snapshot_paths))
    
    # Read and encode images in base64
    snapshot_images = []
    for path in snapshot_paths:
        with open(path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            snapshot_images.append(encoded_string)
    
    return JSONResponse(content={"snapshots": snapshot_images})

@app.get("/api/videos")
async def get_video():
    try:
        # Check if the video file exists
        if not os.path.exists(VIDEO_PATH):
            return dict(status_code=404, detail="Video not found")

        # Return the video file
        return FileResponse(VIDEO_PATH, media_type='video/mp4')
    except Exception as e:
        return {"data": e.args}
