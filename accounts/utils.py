import face_recognition
import cv2
import numpy as np
import os
from django.conf import settings
from PIL import Image

temp_path = os.path.join(settings.BASE_DIR, "media/temp/temp.jpg")


# def extract_face_haar_cascade(image_path):
#     image = cv2.imread(image_path)
#     if image is None:
#         print(f"Failed to load image from path: {image_path}")
#         return None

#     # Convert the image from BGR to RGB (required by face_recognition library)
#     rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

#     # Detect face locations in the image
#     face_locations = face_recognition.face_locations(rgb_image)
#     # face_encodings = face_recognition.face_encodings(face_locations)

#     if len(face_locations) == 0:
#         print("No faces found in the image")
#         return None

#     # Extract the first face bounding box coordinates
#     top, right, bottom, left = face_locations[0]

#     # Crop the face part from the original image
#     face_part = image[top:bottom, left:right]

#     # Convert the face part to RGB color space
#     face_part_rgb = cv2.cvtColor(face_part, cv2.COLOR_BGR2RGB)

#     # Convert the face part to NumPy array
#     face_np_array = np.array(face_part_rgb)


#     return face_np_array


def extract_face_haar_cascade(image_path):
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Failed to load image from path: {image_path}")
        return None
    # Convert the image to grayscale for face detection
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Load the pre-trained Haar Cascade classifier for face detection
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    # Detect faces in the image
    faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.3, minNeighbors=5)

    if len(faces) == 0:
        print("No faces found in the image")
        return None

    # Extract the first detected face
    x, y, w, h = faces[0]

    # Crop the face from the original image
    face_part = image[y : (y + h), x : (x + w)]
    print(face_part.shape)

    # Convert to RGB
    face_part_rgb = cv2.cvtColor(face_part, cv2.COLOR_BGR2RGB)

    # Convert to NumPy array
    face_np_array = np.array(face_part_rgb)

    return face_np_array


def extract_face_haar_cascade2(user_face):
    try:
        # Open the uploaded image using Pillow
        image = Image.open(user_face)

        # Convert the Pillow Image to a NumPy array
        image_np_array = np.array(image)

        # Convert the image from BGR to RGB (required by face_recognition library)
        rgb_image = cv2.cvtColor(image_np_array, cv2.COLOR_BGR2RGB)

        # Detect face locations in the image
        face_locations = face_recognition.face_locations(rgb_image)

        if len(face_locations) == 0:
            print("No faces found in the image")
            return None

        # Extract the first face bounding box coordinates
        top, right, bottom, left = face_locations[0]

        # Crop the face part from the original image
        face_part = image_np_array[top:bottom, left:right]

        # Convert the face part to RGB color space
        face_part_rgb = cv2.cvtColor(face_part, cv2.COLOR_BGR2RGB)

        # Convert the face part to NumPy array
        face_np_array = np.array(face_part_rgb)

        return face_np_array

    except Exception as e:
        print(f"Error processing image: {e}")
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
    # processed_img = resize_image(processed_img, 0.5)
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


def resize(img_path, size):
    img = face_recognition.load_image_file(img_path)
    width = int(img.shape[1] * size)
    height = int(img.shape[0] * size)
    dimension = (width, height)
    return cv2.resize(img, dimension, interpolation=cv2.INTER_AREA)


def resize_image(image, scale_factor):
    width = int(image.shape[1] * scale_factor)
    height = int(image.shape[0] * scale_factor)
    dimension = (width, height)
    resized_image = cv2.resize(image, dimension, interpolation=cv2.INTER_AREA)
    return resized_image
