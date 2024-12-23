import os
import cv2
import json
import numpy as np
import django

# Set up Django settings (Correct project name: Face_Recognition)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Face_Recognition.settings')
django.setup()

from face_app.models import Person

# Directories for saving images and the face recognizer model
image_dir = 'static/images'
model_path = 'face_recognizer_model.yml'
label_info_file = 'label_info.json'

# Create necessary directories and files
if not os.path.exists(image_dir):
    os.makedirs(image_dir)

if not os.path.exists(label_info_file):
    with open(label_info_file, 'w') as f:
        json.dump({}, f)

# Load or initialize label-to-name mapping
with open(label_info_file, 'r') as f:
    label_info_map = json.load(f)

# Load the Haar Cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def detect_face(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)
    if len(faces) == 0:
        return None, None
    (x, y, w, h) = faces[0]
    return gray[y:y+h, x:x+w], (x, y, w, h)

def capture_images(name, roll_number, image_count=60):
    video_capture = cv2.VideoCapture(0)
    images = []
    label = len(label_info_map) + 1  # Assign a new label
    label_info_map[label] = f"{name} ({roll_number})"

    # Save updated label-info mapping
    with open(label_info_file, 'w') as f:
        json.dump(label_info_map, f)

    print("Look at the camera and press 'q' to capture an image. Press 'Esc' to finish.")
    count = 0

    while count < image_count:
        ret, frame = video_capture.read()
        if not ret:
            print("Failed to capture frame.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        cv2.imshow('Capturing Images', frame)

        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q'):
            if len(faces) > 0:
                (x, y, w, h) = faces[0]
                cropped_face = gray[y:y+h, x:x+w]
                face_filename = os.path.join(image_dir, f"{label}_{count}.jpg")
                cv2.imwrite(face_filename, cropped_face)
                images.append(face_filename)
                count += 1
                print(f"Captured image {count}/{image_count}")
            else:
                print("No face detected. Try again.")

        elif key == 27:  # 'Esc' key to exit
            print("User interrupted capture process.")
            break

    video_capture.release()
    cv2.destroyAllWindows()
    return images

def save_to_db(name, roll_number, image_paths):
    try:
        person = Person(name=name, roll_number=roll_number, image_path=json.dumps(image_paths))
        person.save()
    except Exception as e:
        print(f"Error saving to database: {e}")

def prepare_training_data(folder):
    faces, labels = [], []
    for filename in os.listdir(folder):
        if not filename.endswith(".jpg"):
            continue
        label = int(filename.split('_')[0])  # Extract label from filename
        img_path = os.path.join(folder, filename)
        image = cv2.imread(img_path)
        face, rect = detect_face(image)
        if face is not None:
            faces.append(face)
            labels.append(label)
    return faces, np.array(labels)

def train_face_recognizer():
    print("Preparing training data...")
    faces, labels = prepare_training_data(image_dir)

    # Create and train the LBPH face recognizer
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_recognizer.train(faces, labels)

    # Save the trained model
    face_recognizer.save(model_path)
    print(f"Training complete and model saved to {model_path}")

def main():
    name = input("Enter the person's name: ")
    roll_number = input("Enter the roll number: ")
    images = capture_images(name, roll_number)
    save_to_db(name, roll_number, images)
    train_face_recognizer()

if __name__ == "__main__":
    main()
