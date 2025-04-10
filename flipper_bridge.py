import serial
import time
import os
from usb_manager import find_flipper_port

BAUD_RATE = 115200
TIMEOUT = 2

class FlipperBridge:
    def __init__(self, baud=BAUD_RATE):
        port = find_flipper_port()
        if not port:
            print("[ZARN] Flipper not detected.")
            self.ser = None
            return

        try:
            self.ser = serial.Serial(port, baudrate=baud, timeout=TIMEOUT)
            time.sleep(1.5)
            print(f"[ZARN] Connected to Flipper on {port}")
        except Exception as e:
            print(f"[ZARN] Failed to connect to Flipper: {e}")
            self.ser = None

    def is_connected(self):
        return self.ser is not None and self.ser.is_open

    def send_command(self, cmd):
        if not self.is_connected():
            return "[ZARN] Flipper not connected."

        self.ser.write((cmd + "\r\n").encode())
        time.sleep(0.3)
        output = ""
        while self.ser.in_waiting:
            output += self.ser.read(self.ser.in_waiting).decode(errors="ignore")
            time.sleep(0.1)
        return output.strip()

    def send_ir_signal(self, signal_name):
        cmd = f"ir send {signal_name}"
        return self.send_command(cmd)

    def list_storage(self):
        return self.send_command("storage list")

    def close(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
