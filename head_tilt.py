import RPi.GPIO as GPIO
import time
import json
import os

# === CONFIG ===
SERVO_PIN = 18           # GPIO pin connected to the servo signal wire
PWM_FREQ = 50            # Servo PWM frequency
TILT_FILE = "tilt_angle.json"
MIN_ANGLE = 30           # Adjust this based on physical limits
MAX_ANGLE = 150
DEFAULT_ANGLE = 90       # Center position

GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)
pwm = GPIO.PWM(SERVO_PIN, PWM_FREQ)
pwm.start(0)

def angle_to_duty(angle):
    return 2 + (angle / 18.0)  # Converts angle to duty cycle

def save_tilt(angle):
    with open(TILT_FILE, "w") as f:
        json.dump({"angle": angle}, f)

def load_tilt():
    if os.path.exists(TILT_FILE):
        with open(TILT_FILE, "r") as f:
            return json.load(f).get("angle", DEFAULT_ANGLE)
    return DEFAULT_ANGLE

def set_tilt(angle, smooth=True):
    angle = max(MIN_ANGLE, min(MAX_ANGLE, angle))
    current = load_tilt()
    steps = 1 if not smooth else abs(int(angle - current))

    for i in range(steps + 1):
        step_angle = current + ((angle - current) * i / steps)
        pwm.ChangeDutyCycle(angle_to_duty(step_angle))
        time.sleep(0.02)

    save_tilt(angle)
    pwm.ChangeDutyCycle(0)

def tilt_up(degrees=10):
    current = load_tilt()
    set_tilt(current - degrees)

def tilt_down(degrees=10):
    current = load_tilt()
    set_tilt(current + degrees)

def center_head():
    set_tilt(DEFAULT_ANGLE)

def track_face(y_pos, frame_height):
    """
    Adjust tilt based on vertical position of face in frame
    y_pos: center Y coordinate of detected face
    frame_height: total height of camera frame
    """
    center = frame_height / 2
    diff = y_pos - center
    step = int(diff / (frame_height / 30))  # Sensitivity scale
    current = load_tilt()
    set_tilt(current + step)

def cleanup():
    pwm.stop()
    GPIO.cleanup()
