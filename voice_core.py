import speech_recognition as sr import pyttsx3 from video_viewer import handle_voice_command

engine = pyttsx3.init() recognizer = sr.Recognizer()

def speak(text): print("[ZARN]:", text) engine.say(text) engine.runAndWait()

def listen(): with sr.Microphone() as source: print("[ZARN]: Listening...") audio = recognizer.listen(source) try: command = recognizer.recognize_google(audio) print("[You]:", command) return command except sr.UnknownValueError: speak("Sorry, I didn't catch that.") except sr.RequestError as e: speak("Speech recognition service is unavailable.") return ""

def handle_command(command): response = handle_voice_command(command) if response: speak(response) else: speak("I'm not sure how to handle that yet.")

if name == 'main': while True: voice_input = listen() if voice_input: handle_command(voice_input)

