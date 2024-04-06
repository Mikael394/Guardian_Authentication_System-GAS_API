import cv2
from django.core.files.base import ContentFile
from models import Video
import numpy as np

cap = cv2.VideoCapture(0)

# Initialize a variable to store the video frames
video_frames = []

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Convert frame to bytes
    _, buffer = cv2.imencode('.jpg', frame)
    frame_bytes = buffer.tobytes()
    video_frames.append(frame_bytes)

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Convert list of frame bytes to a single byte array
video_data = b''.join(video_frames)

cap.release()
cv2.destroyAllWindows()

# Create a Video instance and save the video data to it
video = Video()
video.file.save('my_video.mp4', ContentFile(video_data), save=True)
