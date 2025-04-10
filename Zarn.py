import os
import json
from modules.voice_core import speak
from modules.memory import load_memory, save_memory

ZARN_DIR = os.path.dirname(os.path.abspath(__file__))
MEMORY_FILE = os.path.join(ZARN_DIR, 'zarn_memory.json')

def startup():
    speak("Zarn online.")
    memory = load_memory(MEMORY_FILE)
    if "last_boot" in memory:
        speak("Last boot was at " + memory["last_boot"])
    memory["last_boot"] = os.popen("date").read().strip()
    save_memory(MEMORY_FILE, memory)

if __name__ == "__main__":
    startup()
