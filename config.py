# head_tilt.py
import RPi.GPIO as GPIO
import time
import config

GPIO.setmode(GPIO.BCM)
GPIO.setup(config.SERVO_PIN, GPIO.OUT)

servo = GPIO.PWM(config.SERVO_PIN, 50)  # 50Hz
servo.start(0)

def angle_to_duty(angle):
    return (angle / 18.0) + 2.5

def set_tilt(angle):
    angle = max(min(angle, config.SERVO_MAX_ANGLE), config.SERVO_MIN_ANGLE)
    duty = angle_to_duty(angle)
    servo.ChangeDutyCycle(duty)
    time.sleep(0.3)
    servo.ChangeDutyCycle(0)

def center_head():
    set_tilt(config.SERVO_CENTER_ANGLE)

def cleanup():
    servo.stop()
    GPIO.cleanup()
