import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import random
import openai

# Set your OpenAI API key here
openai.api_key = 'YOUR_OPENAI_API_KEY'

# Initialize speech recognition
recognizer = sr.Recognizer()

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Function to convert text to speech
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to greet user
def greet():
    current_hour = datetime.datetime.now().hour
    if 6 <= current_hour < 12:
        speak("Good morning!")
    elif 12 <= current_hour < 18:
        speak("Good afternoon!")
    elif 18 <= current_hour < 24:
        speak("Good evening!")
    else:
        speak("Hello!")
    speak("I'm your personal assistant. How can I help you today?")

# Function to take command from user
def take_command():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        try:
            print("Recognizing...")
            query = recognizer.recognize_google(audio, language='en-US')
            print(f"User said: {query}\n")
        except Exception as e:
            print("Sorry, I didn't get that. Please try again.")
            return None

    return query.lower()

# Function to handle different commands
def handle_command(command):
    if 'wikipedia' in command:
        speak("Searching Wikipedia...")
        command = command.replace("wikipedia", "")
        results = wikipedia.summary(command, sentences=2)
        speak("According to Wikipedia")
        speak(results)

    elif 'open youtube' in command:
        speak("Opening YouTube...")
        webbrowser.open("https://www.youtube.com")

    elif 'open google' in command:
        speak("Opening Google...")
        webbrowser.open("https://www.google.com")

    elif 'play music' in command:
        speak("Playing music...")
        music_dir = 'C:\\Music'  # Change this to your music directory
        songs = os.listdir(music_dir)
        os.startfile(os.path.join(music_dir, random.choice(songs)))

    elif 'the time' in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}")

    elif 'answer' in command:
        question = command.split('answer')[-1].strip()
        speak("Let me find the answer for you...")
        answer = openai.Completion.create(
            engine="davinci",
            prompt=question,
            max_tokens=50
        )
        speak(answer.choices[0].text.strip())

    elif 'quit' in command or 'exit' in command:
        speak("Goodbye!")
        exit()

    else:
        speak("I'm sorry, I don't understand that command.")

# Main function to execute commands
def main():
    greet()

    while True:
        command = take_command()

        if command:
            handle_command(command)

if __name__ == "__main__":
    main()
