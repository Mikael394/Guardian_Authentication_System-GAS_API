import cv2
import os
import tempfile
from django.core.files import File
from accounts.models import Video  # Import your Django model

def record_and_upload_video():
    # OpenCV Video Capture
    cap = cv2.VideoCapture(0)  # 0 for default camera

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))  # Change resolution if needed

    # Record video for 10 seconds
    seconds_to_record = 10
    while cap.isOpened() and seconds_to_record > 0:
        ret, frame = cap.read()
        if ret:
            out.write(frame)
            seconds_to_record -= 1
        else:
            break

    # Release everything if job is finished
    cap.release()
    out.release()
    cv2.destroyAllWindows()

    # Save video file to Django database
    with open('output.avi', 'rb') as f:
        video_temp = tempfile.NamedTemporaryFile(delete=True)
        video_temp.write(f.read())
        video_temp.flush()
        video_model = Video()
        video_model.file.save('output.avi', File(video_temp), save=True)

    # Clean up temporary file
    os.remove('output.avi')

    print("Video recorded and uploaded successfully!")

# Example Django model
# Assuming you have a model named Video with a field 'video_field' to store the video
# class Video(models.Model):
#     video_field = models.FileField(upload_to='videos/')

# Call the function
