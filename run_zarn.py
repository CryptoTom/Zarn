
from voice_core import VoiceCore
from zarn_api import ZarnAPI
import json

with open("zarn_secrets.json") as f:
    secrets = json.load(f)

zarn = Zarn(api_key=secrets["openai_api_key"])
voice = VoiceCore()
api = ZarnAPI(zarn)

def start_zarn():
    voice.speak("Zarn online.")
    while True:
        text = voice.listen()
        if not text:
            continue
        if text.lower() in ["sleep", "power down"]:
            voice.speak("Going to sleep.")
            break
        reply = api.chat(text)
        voice.speak(reply)

if __name__ == "__main__":
    start_zarn()
