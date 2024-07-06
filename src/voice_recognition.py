import speech_recognition as sr
import pyttsx3

recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()

def recognize_speech():
    with sr.Microphone() as source:
        audio = recognizer.listen(source)
        try:
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            return "Sorry, I did not understand that."
        except sr.RequestError:
            return "Sorry, my speech service is down."

def synthesize_speech(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

# Example usage
print("Say something:")
user_message = recognize_speech()
print(f"You said: {user_message}")
synthesize_speech("Hello, how can I help you?")