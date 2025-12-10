"""
assistant.py
A simple Python voice assistant (PC) that:
 - greets the user
 - listens for voice commands (using microphone)
 - can say text, tell time, search wikipedia, open websites, play youtube via webbrowser/pywhatkit, tell jokes
 - uses a wake phrase ("hello python") to start
Works on Python 3.8+.

Notes:
 - Uses the SpeechRecognition library with Google Web Speech API (online).
 - Uses pyttsx3 for offline TTS (no API key).
 - pywhatkit is used to play YouTube videos (opens browser).
"""

import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import pyjokes
import sys
import traceback

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # speech rate

def speak(text: str):
    """Speak the given text and also print it."""
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

def wish_user():
    hour = datetime.datetime.now().hour
    if hour < 12:
        speak("Good morning!")
    elif hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")
    speak("I am your assistant. Say 'hello python' to activate me.")

def listen_once(timeout=5, phrase_time_limit=8):
    """Listen from microphone and return recognized text or None."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=0.6)
        try:
            audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
        except sr.WaitTimeoutError:
            return None

    try:
        text = r.recognize_google(audio)
        print("You:", text)
        return text.lower()
    except sr.UnknownValueError:
        return None
    except sr.RequestError as e:
        speak("Network/API error. Check your internet connection.")
        print("Speech recognition Request Error:", e)
        return None

def take_command_loop():
    """Main loop: waits for wake phrase and then accepts commands."""
    wish_user()
    while True:
        try:
            text = listen_once(timeout=8, phrase_time_limit=6)
            if not text:
                continue

            # Wake phrase
            if "hello python" in text or "hey python" in text:
                speak("Yes, I am listening. How can I help?")
                # After wake, listen for a command
                cmd = listen_once(timeout=6, phrase_time_limit=8)
                if not cmd:
                    speak("I didn't catch that. Please say again.")
                    continue

                # Commands
                if "wikipedia" in cmd:
                    speak("Searching Wikipedia...")
                    try:
                        query = cmd.replace("wikipedia", "").strip()
                        if not query:
                            speak("What should I search on Wikipedia?")
                            query = listen_once(timeout=6, phrase_time_limit=6) or ""
                        summary = wikipedia.summary(query, sentences=2)
                        speak("According to Wikipedia")
                        speak(summary)
                    except Exception as e:
                        speak("Sorry, I couldn't fetch from Wikipedia.")
                        print("Wikipedia error:", e)

                elif "open youtube" in cmd or "play youtube" in cmd:
                    speak("What should I play on YouTube?")
                    q = listen_once(timeout=6, phrase_time_limit=6) or ""
                    if q:
                        # use webbrowser to search YouTube
                        url = f"https://www.youtube.com/results?search_query={q.replace(' ', '+')}"
                        webbrowser.open(url)
                        speak(f"Playing {q} on YouTube")
                    else:
                        speak("No query provided.")

                elif "open google" in cmd:
                    webbrowser.open("https://www.google.com")
                    speak("Opening Google")

                elif "time" in cmd:
                    now = datetime.datetime.now().strftime("%I:%M %p")
                    speak(f"The time is {now}")

                elif "joke" in cmd or "tell me a joke" in cmd:
                    joke = pyjokes.get_joke()
                    speak(joke)

                elif "type" in cmd or "text to speech" in cmd:
                    # simple text to speech from typed input
                    speak("Please type the text you want me to speak. Press Enter when done.")
                    user_text = input("Text to speak: ")
                    if user_text.strip():
                        speak(user_text.strip())
                    else:
                        speak("No text provided.")

                elif "quit" in cmd or "exit" in cmd or "stop" in cmd:
                    speak("Goodbye!")
                    break

                else:
                    # fallback: try opening a website if command contains 'open' word
                    if "open" in cmd:
                        parts = cmd.split()
                        try:
                            idx = parts.index("open")
                            site = parts[idx + 1]
                            if "." not in site:
                                site = site + ".com"
                            url = "https://" + site
                            webbrowser.open(url)
                            speak(f"Opening {site}")
                        except Exception:
                            speak("Sorry I couldn't open that site.")
                    else:
                        speak("I didn't understand that command. Try: wikipedia, open youtube, time, joke, quit.")
            # allow keyboard quit
            if "exit program" in text or "shutdown" in text:
                speak("Shutting down. Bye.")
                break

        except KeyboardInterrupt:
            speak("Interrupted by user. Exiting.")
            break
        except Exception:
            speak("An error occurred. Check the console for details.")
            traceback.print_exc()
            break

if __name__ == "__main__":
    try:
        take_command_loop()
    except Exception as e:
        print("Fatal error:", e)
        sys.exit(1)
