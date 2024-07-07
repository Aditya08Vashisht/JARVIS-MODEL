
import speech_recognition as sr
import webbrowser
import pyttsx3
import time
import musiclib



recognizer = sr.Recognizer() 
engine = pyttsx3.init()

def speak(text):
    print(f"Jarvis: {text}")
    engine.say(text)
    engine.runAndWait()

def processCommand(command):
    print(f"Processing command: {command}")
    command = command.lower()
    try:
        if "open google" in command:
            print("Opening Google")
            speak("Opening Google")
            webbrowser.open('https://www.google.com')
        elif "open facebook" in command:
            print("Opening Facebook")
            speak("Opening Facebook")
            webbrowser.open('https://www.facebook.com')
        elif "open youtube" in command:
            print("Opening YouTube")
            speak("Opening YouTube")
            webbrowser.open('https://www.youtube.com')
        elif command.startswith("play "):
            song = command.split("play ", 1)[1]
            link = musiclib.music.get(song)
            if link:
                speak(f"Playing {song}")
                webbrowser.open(link)
            else:
                speak(f"Song {song} not found in the music library.")
        else:
            speak("Command not recognized.")
    except Exception as e:
        print(f"Error in processCommand: {e}")
        speak("An error occurred while processing your command.")

def listenForCommand():
    with sr.Microphone() as source:
        print("Listening for command...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source, timeout=4, phrase_time_limit=2)
    try:
        command = recognizer.recognize_google(audio).lower()
        print(f"Recognized command: {command}")
        return command
    except sr.UnknownValueError:
        print("Could not understand command")
        return None
    except sr.RequestError:
        print("Could not request results from Google Speech Recognition service")
        return None

if __name__ == "__main__":
    speak("Initializing Jarvis...")
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening for wake word...")
                recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
            word = recognizer.recognize_google(audio).lower()
            print(f"Recognized: {word}")
            if "jarvis" in word:
                speak("Yes, how can I help you?")
                
                # Try to get a command up to 3 times
                for _ in range(3):
                    command = listenForCommand()
                    if command:
                        processCommand(command)
                        break
                    else:
                        speak("I didn't catch that. Could you please repeat?")
                else:
                    speak("I'm having trouble understanding. Let's try again later.")
            else:
                print("Wake word not recognized")
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
        except Exception as e:
            print(f"Error: {e}")
        
        time.sleep(1)  # Add a small delay to prevent excessive CPU usage

