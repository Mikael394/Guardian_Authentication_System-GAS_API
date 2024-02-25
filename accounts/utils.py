import face_recognition
import cv2
import numpy as np
import os
from django.conf import settings
from PIL import Image
from io import BytesIO

temp_path = os.path.join(settings.BASE_DIR, "media/temp/temp.jpg")

def extract_face_haar_cascade(image_path):
    try:
        # Load the image
        image = cv2.imread(image_path)
        
        # Check if the image was loaded successfully
        if image is None:
            raise ValueError(f"Failed to load image from path: {image_path}")

        # Convert the image to grayscale for face detection
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Load the pre-trained Haar Cascade classifier for face detection
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )

        # Detect faces in the image
        faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.4, minNeighbors=5)

        if len(faces) == 0:
            print("No faces found in the image")
            return None

        # Extract the first detected face
        x, y, w, h = faces[0]

        # Crop the face from the original image
        face_part = image[y : (y + h), x : (x + w)]

        # Convert to RGB
        face_part_rgb = cv2.cvtColor(face_part, cv2.COLOR_BGR2RGB)

        # Convert to NumPy array
        face_np_array = np.array(face_part_rgb)

        return face_np_array

    except Exception as e:
        print(f"Error occurred: {e}")
        return None

def image_to_numpy(image_data):
    # Load image from binary data
    image = Image.open(BytesIO(image_data))
    # Convert image to numpy array
    image_array = np.array(image)
    return image_array

def extract_face_haar_cascade3(image):
    try:
        # Convert the image to grayscale for face detection
        gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

        # Load the pre-trained Haar Cascade classifier for face detection
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

        # Detect faces in the image
        faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.4, minNeighbors=5)

        if len(faces) == 0:
            print("No faces found in the image")
            return None

        # Extract the first detected face
        x, y, w, h = faces[0]

        # Crop the face from the original image
        face_part = image[y : (y + h), x : (x + w)]

        return face_part

    except Exception as e:
        print(f"Error occurred: {e}")
        return None


def save_up(uploaded_image):
    try:
        with open(temp_path, "wb+") as destination_file:
            for chunk in uploaded_image.chunks():
                destination_file.write(chunk)
    except IOError as e:
        # Handle the error appropriately
        print(f"Error saving image: {e}")
        return False
    processed_img = extract_face_haar_cascade(temp_path)
    if processed_img is None:
        return None
    pil_image = Image.fromarray(processed_img)
    pil_image.save(temp_path)
    return temp_path



def compare(path1, path2):
    image1 = face_recognition.load_image_file(path1)
    image2 = face_recognition.load_image_file(path2)

    image_encoding1 = face_recognition.face_encodings(image1)
    image_encoding2 = face_recognition.face_encodings(image2)

    result = face_recognition.compare_faces(
        [image_encoding1[0]], image_encoding2[0], tolerance=0.5
    )
    print(result)
    return result[0]

def compare2(path1, image2):
    image1 = face_recognition.load_image_file(path1)
    # image2 = face_recognition.load_image_file(path2)

    image_encoding1 = face_recognition.face_encodings(image1)
    image_encoding2 = face_recognition.face_encodings(image2)

    result = face_recognition.compare_faces(
        [image_encoding1[0]], image_encoding2[0], tolerance=0.5
    )
    print(result)
    return result[0]
