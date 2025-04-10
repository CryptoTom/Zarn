import pyttsx3
import queue
import sounddevice as sd
import vosk
import sys
import json
from zarn_api import ask_axis

q = queue.Queue()
model = vosk.Model("model")  # Download Vosk model and place in /model
engine = pyttsx3.init()

def speak(text):
    print("ZARN:", text)
    engine.say(text)
    engine.runAndWait()

def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

def listen():
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        rec = vosk.KaldiRecognizer(model, 16000)
        print("Listening... Say 'ZARN' to wake up.")
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                text = result.get("text", "")
                if "zarn" in text.lower():
                    speak("Yes?")
                    return capture_command()

def capture_command():
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        rec = vosk.KaldiRecognizer(model, 16000)
        print("Listening for command...")
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                command = result.get("text", "")
                return command

if __name__ == "__main__":
    while True:
        user_input = listen()
        reply = ask_axis(user_input)
        speak(reply)
