import cv2
import face_recog
import head_tilt
import config
from datetime import datetime, timedelta
import json
import os

LOG_FILE = "face_log.json"
GREETING_INTERVAL_HOURS = 3

def load_greet_log():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            return json.load(f)
    return {}

def update_greet_log(name):
    log = load_greet_log()
    log[name] = datetime.now().isoformat()
    with open(LOG_FILE, "w") as f:
        json.dump(log, f)

def should_greet(name):
    log = load_greet_log()
    if name not in log:
        return True
    last_seen = datetime.fromisoformat(log[name])
    return datetime.now() - last_seen > timedelta(hours=GREETING_INTERVAL_HOURS)

# === Setup ===
face_recog.load_known_faces()
cap = cv2.VideoCapture(config.CAMERA_INDEX)

print("[ZARN] Facial tracking engaged.")

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        names, locations = face_recog.recognize_faces(frame)

        for (name, (top, right, bottom, left)) in zip(names, locations):
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, top - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

            # Head tilt tracking
            y_center = (top + bottom) // 2
            head_tilt.track_face(y_center, frame.shape[0])

            # Greet if eligible
            if name != "Unknown" and should_greet(name):
                print(f"[ZARN] Hi {name}")
                update_greet_log(name)

        cv2.imshow("ZARN Face Tracker", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
    head_tilt.cleanup()
    print("[ZARN] Shutdown complete.")
