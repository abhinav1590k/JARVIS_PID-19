# Importing required libraries
import speech_recognition as sr       # For speech recognition
import pyttsx3                        # For text-to-speech conversion

# Initialize the pyttsx3 engine (used to convert text to speech)
engine = pyttsx3.init()

def speak(text):
    """Speak the given text using pyttsx3 engine."""
    print(f"Jarvis: {text}")         # Print text to console for debugging
    engine.say(text)                 # Queue the text to be spoken
    engine.runAndWait()              # Speak the queued text

def listen():
    """Listen to the user's voice and recognize the command."""
    r = sr.Recognizer()              # Create a Recognizer instance to recognize speech

    with sr.Microphone() as source:             # Use the default system microphone as the audio source
        print("Listening...")                   # Debug print to show it's listening
        speak("Listening for your command...")  # Speak prompt to user

        r.adjust_for_ambient_noise(source)      # Adjust for background noise for better accuracy
        audio = r.listen(source)                # Listen and store audio from the user

        try:
            # Try to recognize the speech using Google’s speech recognition
            command = r.recognize_google(audio)     # Convert audio to text
            print(f"User said: {command}")           # Print the recognized text for debugging
            return command.lower()                  # Return the command in lowercase for uniform processing

        except sr.UnknownValueError:
            # If speech was not understood (garbled or unclear)
            speak("Sorry, I didn't understand that. Could you repeat?")
            return ""  # Return an empty string

        except sr.RequestError:
            # If there's an issue with the recognition service (e.g., no internet)
            speak("Sorry, there was an error with the speech recognition service.")
            return ""  # Return an empty string
