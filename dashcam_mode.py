import cv2 import os import datetime import threading

SAVE_PATH = "/home/pi/zarn/dashcam" MAX_DAYS = 7  # auto-delete videos older than this FPS = 15

os.makedirs(SAVE_PATH, exist_ok=True)

def get_filename(): now = datetime.datetime.now() date_folder = os.path.join(SAVE_PATH, now.strftime("%Y-%m-%d")) os.makedirs(date_folder, exist_ok=True) return os.path.join(date_folder, now.strftime("%H-%M-%S") + ".mp4")

def cleanup_old(): now = datetime.datetime.now() for folder in os.listdir(SAVE_PATH): full_path = os.path.join(SAVE_PATH, folder) if os.path.isdir(full_path): folder_date = datetime.datetime.strptime(folder, "%Y-%m-%d") if (now - folder_date).days > MAX_DAYS: os.system(f"rm -rf '{full_path}'")

def dashcam_loop(): cap = cv2.VideoCapture(0) if not cap.isOpened(): print("Camera not available") return

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

while True:
    filename = get_filename()
    out = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*'mp4v'), FPS, (width, height))
    print(f"Recording {filename}...")

    for _ in range(FPS * 60 * 5):  # 5-minute chunks
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)

    out.release()
    cleanup_old()

cap.release()

def start_dashcam(): threading.Thread(target=dashcam_loop, daemon=True).start()

if name == 'main': start_dashcam() input("Dashcam recording. Press Enter to stop.\n")

