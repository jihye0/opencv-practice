# Import necessary libraries
import cv2
import numpy as np
import os
import urllib.request

# Function to apply Gaussian blur to an image
def apply_blur(img, k):
    return cv2.GaussianBlur(img, (k, k), 0)

# Function to pixelate a specific region in an image
def pixelate_region(image, startX, startY, endX, endY, blocks=10):
    region = image[startY:endY, startX:endX]
    (h, w) = region.shape[:2]
    block_size = (w // blocks, h // blocks)
    for y in range(0, h, block_size[1]):
        for x in range(0, w, block_size[0]):
            roi = region[y:y + block_size[1], x:x + block_size[0]]
            color = np.mean(roi, axis=(0, 1), dtype=int)
            cv2.rectangle(region, (x, y), (x + block_size[0], y + block_size[1]), color.tolist(), -1)
    image[startY:endY, startX:endX] = region

# Function to pixelate the face in an image
def pixelate_face(image, blocks=10):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 얼굴 검출
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    for (x, y, w, h) in faces:
        pixelate_region(image, x, y, x + w, y + h, blocks)

# Function to download the Haarcascade file if not exists
def download_haarcascade_file():
    url = 'https://github.com/opencv/opencv/raw/master/data/haarcascades/haarcascade_frontalface_default.xml'
    filename = 'haarcascade_frontalface_default.xml'
    if not os.path.exists(filename):
        print(f"Downloading {filename}...")
        urllib.request.urlretrieve(url, filename)
        print(f"{filename} downloaded successfully.")
        

if __name__ == "__main__":
    # Download Haarcascade file if not exists
    #download_haarcascade_file()
    # Load the Haarcascade classifier for face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    # Capture video stream and apply pixelation to detected faces
    cap = cv2.VideoCapture(1)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        # Apply pixelation effect to detected faces
        pixelate_face(frame, blocks=10)
        # Display the result
        cv2.imshow('Pixelated Face Detection', frame)
        # Exit loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    # Release the camera and close all windows
    cap.release()
    cv2.destroyAllWindows()