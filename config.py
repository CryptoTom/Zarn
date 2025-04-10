# config.py

# --- Hardware Pins ---
SERVO_PIN = 18  # PWM pin for head tilt
RELAY_PIN = 17  # Optional: pin for relay control

# --- Camera ---
CAMERA_INDEX = 0  # 0 = default PiCam/USB cam

# --- Servo Settings ---
SERVO_MIN_ANGLE = 60
SERVO_MAX_ANGLE = 120
SERVO_CENTER_ANGLE = 90

# --- Wake Word ---
WAKE_WORD = "zarn"

# --- Paths ---
MEMORY_FILE = "zarn_memory.json"
SECRETS_FILE = "zarn_secrets.json"

# --- Face Recognition ---
KNOWN_FACES_DIR = "known_faces"
UNKNOWN_FACES_DIR = "unknown_faces"

# --- Debug Flags ---
DEBUG = True
LOGGING_ENABLED = True

# --- API/Network Settings ---
USE_FLIPPER = True
USE_CLOUD = True
