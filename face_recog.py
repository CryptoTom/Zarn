import cv2
import face_recognition
import os
import json
from datetime import datetime, timedelta

KNOWN_FACES_DIR = "known_faces"
LOG_FILE = "face_log.json"
GREETING_INTERVAL_HOURS = 3

if not os.path.exists(KNOWN_FACES_DIR):
    os.makedirs(KNOWN_FACES_DIR)

if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w") as f:
        json.dump({}, f)

def load_known_faces():
    known_encodings = []
    known_names = []
    for filename in os.listdir(KNOWN_FACES_DIR):
        path = os.path.join(KNOWN_FACES_DIR, filename)
        image = face_recognition.load_image_file(path)
        encoding = face_recognition.face_encodings(image)
        if encoding:
            known_encodings.append(encoding[0])
            known_names.append(os.path.splitext(filename)[0])
    return known_encodings, known_names

def load_log():
    with open(LOG_FILE, "r") as f:
        return json.load(f)

def update_log(name):
    log = load_log()
    log[name] = datetime.now().isoformat()
    with open(LOG_FILE, "w") as f:
        json.dump(log, f)

def should_greet(name):
    log = load_log()
    if name not in log:
        return True
    last_seen = datetime.fromisoformat(log[name])
    return datetime.now() - last_seen > timedelta(hours=GREETING_INTERVAL_HOURS)

def recognize_faces():
    encodings, names = load_known_faces()
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb)
        face_encodings = face_recognition.face_encodings(rgb, face_locations)

        for encoding in face_encodings:
            matches = face_recognition.compare_faces(encodings, encoding)
            name = "Unknown"

            if True in matches:
                match_index = matches.index(True)
                name = names[match_index]

                if should_greet(name):
                    print(f"Hi {name}")
                    update_log(name)

        cv2.imshow("ZARN Camera", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    recognize_faces()
