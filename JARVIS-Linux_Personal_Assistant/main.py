# Import required libraries
import tkinter as tk  # For GUI
import subprocess  # To run terminal/system commands
import threading  # To run tasks without freezing GUI
import speech_recognition as sr  # For voice input
import pyttsx3  # For text-to-speech
import webbrowser  # To open web pages

# Initialize the text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 130)  # Set speaking speed (words per minute)
user_name = "Abhinav"  # Hardcoded user name

# Function to make the assistant speak
def speak(text):
    print(f"Jarvis: {text}")  # Print what Jarvis says (for debugging)
    engine.say(text)  # Convert text to speech
    engine.runAndWait()  # Wait until speaking is finished

# Function to run system commands and show the result in GUI
def run_command(command, description):
    result = subprocess.getoutput(command)  # Run command and get output
    output_area.delete(1.0, tk.END)  # Clear previous output in the text area
    output_area.insert(tk.END, f"{description}:\n{result}")  # Display description and result

# Function to identify the user
def identify_user():
    speak(f"You are {user_name} my creator")  # Speak the user's name
    output_area.delete(1.0, tk.END)  # Clear previous output
    output_area.insert(tk.END, f"\nYou are {user_name}, my creator")  # Show in the output area

# Function to capture voice command using microphone
def listen_for_command():
    recognizer = sr.Recognizer()  # Create recognizer object
    with sr.Microphone() as source:  # Use default microphone
        speak("Listening for your command...")  # Speak listening message
        print("Listening...")  # Debug print
        audio = recognizer.listen(source)  # Listen to user voice
        try:
            command = recognizer.recognize_google(audio)  # Convert voice to text using Google API
            print(f"User said: {command}")  # Print command for debugging
            process_voice_command(command)  # Process the recognized command
        except sr.UnknownValueError:
            speak("Sorry, I could not understand what you said.")  # If voice is not clear
        except sr.RequestError:
            speak("Sorry, I couldn't request results from the Google Speech Recognition service.")  # If API error

# Function to process the voice command
def process_voice_command(command):
    command = command.lower().strip()  # Convert to lowercase and remove extra spaces

    # Match commands with predefined actions
    if 'cpu usage' in command:
        speak("Showing CPU usage")
        run_command("top -bn1 | grep 'Cpu(s)'", "CPU Usage")
    elif 'memory usage' in command:
        speak("Showing memory usage")
        run_command("free -h", "Memory Usage")
    elif 'disk usage' in command:
        speak("Showing Disk usage")
        run_command("df -h", "Disk Usage")
    elif 'calendar' in command:
        speak("Here is the calendar")
        run_command("cal", "Calendar")
    elif "who am i" in command or "what's my name" in command:
        speak(f"You are {user_name}, my creator")
    elif "time" in command or "date" in command:
        speak("Fetching current time and date")
        run_command("date", "Current Date and Time")
    elif 'search' in command:
        # Extract search query
        search_query = command.replace("search", "").strip()
        if search_query:
            speak(f"Searching for {search_query} on the web")
            webbrowser.open(f"https://www.google.com/search?q={search_query}")  # Open Google search
        else:
            speak("Please specify what you want to search for.")
    elif 'exit' in command or 'goodbye' in command:
        speak("Goodbye!")
        root.quit()  # Close the GUI
    else:
        speak(f"Sorry, I didn't recognize that command: {command}")  # Unknown command

# Function to start voice command in a separate thread (so GUI doesn't freeze)
def start_listening_thread():
    threading.Thread(target=listen_for_command, daemon=True).start()  # Run in background

# Function to speak goodbye and close the app after a short delay
def speak_and_exit():
    speak("Goodbye see you soon!")
    root.after(1000, root.quit)  # Quit after 1 second delay

# Function to start the GUI
def start_gui():
    print("Starting program...")  # Debug print
    global root
    root = tk.Tk()  # Create the main window
    root.title("JARVIS")  # Set window title

    # Add heading label
    label = tk.Label(root, text="Linux Personal Assistant", font=("Helvetica", 16))
    label.pack(pady=20)

    # Add buttons for different system operations
    tk.Button(root, text="CPU Usage", command=lambda: speak("Fetching cpu usage") or run_command("top -bn1 | grep 'Cpu(s)'", "CPU Usage")).pack(pady=5)
    tk.Button(root, text="Memory Usage", command=lambda: speak("Fetching memory usage") or run_command("free -h", "Memory Usage")).pack(pady=5)
    tk.Button(root, text="Disk Usage", command=lambda: speak("Fetching disk usage") or run_command("df -h", "Disk Usage")).pack(pady=5)
    tk.Button(root, text="Calendar", command=lambda: speak("Fetching calender") or run_command("cal", "Calendar")).pack(pady=5)
    tk.Button(root, text="Date & Time", command=lambda: speak("Fetching current date and time") or run_command("date", "Current Date and Time")).pack(pady=5)
    tk.Button(root, text="Who Am I?", command=identify_user).pack(pady=5)
    tk.Button(root, text="Voice Command", command=start_listening_thread).pack(pady=5)
    tk.Button(root, text="Exit", command=speak_and_exit).pack(pady=5)

    # Add a text area to display output
    global output_area
    output_area = tk.Text(root, height=10, width=50)
    output_area.pack(padx=10, pady=10)

    # Start the GUI event loop
    root.mainloop()
    print("Tkinter main loop ended.")  # Debug print when GUI closes

# Main entry point
if _name_ == "_main_":
    start_gui()  # Start the GUI when script is run directly
