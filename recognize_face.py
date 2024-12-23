import cv2
import os
import numpy as np
import json

# Load the Haar Cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Confidence threshold for face recognition
CONFIDENCE_THRESHOLD = 50  # Lower value means higher confidence

# Load the pre-trained LBPH face recognizer model from the 'static' folder
face_recognizer = cv2.face.LBPHFaceRecognizer_create()
model_path = os.path.join('static', 'face_recognizer_model.yml')

if not os.path.exists(model_path):
    print(f"Model file '{model_path}' not found. Please run the training script first.")
    exit()

face_recognizer.read(model_path)

# Load the label-to-name mapping
label_info_file = 'label_info.json'
if not os.path.exists(label_info_file):
    print(f"Label info file '{label_info_file}' not found. Please run the training script first.")
    exit()

with open(label_info_file, 'r') as f:
    label_info_map = json.load(f)

# Function to detect a face in an image
def detect_face(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)
    if len(faces) == 0:
        return None, None
    (x, y, w, h) = faces[0]
    return gray[y:y+h, x:x+w], (x, y, w, h)

# Function to draw rectangle around the face
def draw_rectangle(img, rect):
    (x, y, w, h) = rect
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

# Function to draw text (name and confidence) on the image
def draw_text(img, text, x, y):
    cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)

# Predict function for recognizing face
def predict(test_img):
    img = test_img.copy()
    face, rect = detect_face(img)
    if face is not None:
        label, confidence = face_recognizer.predict(face)
        if confidence < CONFIDENCE_THRESHOLD:
            name = label_info_map.get(str(label), "Unknown")
            draw_rectangle(img, rect)
            draw_text(img, f"{name}, Conf: {int(confidence)}", rect[0], rect[1] - 5)
        else:
            draw_rectangle(img, rect)
            draw_text(img, "Unknown", rect[0], rect[1] - 5)
    return img

# Start webcam for face recognition
print("Starting face recognition. Press 'e' to quit.")
video_capture = cv2.VideoCapture(0)

while True:
    ret, frame = video_capture.read()
    if not ret:
        print("Failed to capture frame.")
        break

    predicted_img = predict(frame)
    cv2.imshow("Face Recognition", predicted_img)

    if cv2.waitKey(1) & 0xFF == ord('e'):
        print("Exiting face recognition.")
        break

video_capture.release()
cv2.destroyAllWindows()
