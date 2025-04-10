import os

def list_usb_devices():
    try:
        devices = os.listdir('/dev')
        return [dev for dev in devices if 'ttyACM' in dev or 'ttyUSB' in dev]
    except Exception as e:
        return [f"Error: {e}"]

def find_flipper_port():
    possible_ports = list_usb_devices()
    for port in possible_ports:
        path = f"/dev/{port}"
        try:
            with open(path, 'rb'):
                return path
        except:
            continue
    return None

def is_flipper_connected():
    return find_flipper_port() is not None

if __name__ == "__main__":
    print("USB Devices:", list_usb_devices())
    print("Flipper Port:", find_flipper_port())
    print("Connected:", is_flipper_connected())
