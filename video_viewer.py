import os import datetime import subprocess

BASE_DIR = "/home/pi/zarn_recordings"

def get_clip_path(target_datetime): date_str = target_datetime.strftime("%Y-%m-%d") time_str = target_datetime.strftime("%H-%M") folder = os.path.join(BASE_DIR, date_str)

if not os.path.exists(folder):
    return None

for file in os.listdir(folder):
    if time_str in file:
        return os.path.join(folder, file)
return None

def show_clip_from_time(query_time): now = datetime.datetime.now()

if "yesterday" in query_time.lower():
    base_date = now - datetime.timedelta(days=1)
else:
    base_date = now

try:
    raw_time = query_time.lower().replace("am", " am").replace("pm", " pm").replace(":", ":00")
    target_time = datetime.datetime.strptime(raw_time.strip(), "%I:%M %p")
except:
    try:
        target_time = datetime.datetime.strptime(query_time.strip(), "%H:%M")
    except:
        return "Sorry, I couldn’t understand that time."

target_dt = base_date.replace(hour=target_time.hour, minute=target_time.minute, second=0)
path = get_clip_path(target_dt)

if not path:
    return f"No video found for {target_dt.strftime('%Y-%m-%d %I:%M %p')}"

try:
    subprocess.Popen(["xdg-open", path])
    return f"Opening clip from {target_dt.strftime('%I:%M %p')}..."
except Exception as e:
    return f"Failed to play video: {e}"

Voice trigger integration

def handle_voice_command(command): if any(trigger in command.lower() for trigger in ["show me", "play", "open clip"]): parts = command.lower().split("show me") if "show me" in command.lower() else 
command.lower().split("play") if "play" in command.lower() else 
command.lower().split("open clip") if len(parts) > 1: return show_clip_from_time(parts[1].strip()) return None

Hook for voice_core integration

if name == 'main': while True: cmd = input("ZARN (voice sim): ") print(handle_voice_command(cmd))

