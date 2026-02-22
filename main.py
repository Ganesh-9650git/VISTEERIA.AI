import pyttsx3
import speech_recognition as sr
from datetime import datetime
import wikipedia
import webbrowser
import time


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
if voices and len(voices) > 1:
    engine.setProperty('voice', voices[1].id)

engine.setProperty('rate', 200)
engine.setProperty('volume', 0.8)

PASSWORD="1234"
maxm_attempts=3

def speak(audio):
    print(f"VISTEERIA: {audio}")
    engine.say(audio)
    engine.runAndWait()
    time.sleep(0.1)

def authenticate():
    """Voice password authentication system"""
    attempts = 0
    
    speak("Authentication required. Please speak your password.")
    
    while attempts < maxm_attempts:                                  
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print(f"\n🔒 Password Attempt {attempts + 1}/{maxm_attempts}")
            print("Listening for password...")
            
            r.pause_threshold = 1
            r.energy_threshold = 250
            try:
                r.adjust_for_ambient_noise(source, duration=0.5)
            except:
                pass
            
            try:
                audio = r.listen(source, timeout=5, phrase_time_limit=4)
                print("Verifying...")
                
                password_input = r.recognize_google(audio, language='en-in').lower().strip()
                print(f"You said: {password_input}")
                
                # Check if password matches
                if password_input == PASSWORD.lower():
                    engine.say("Access granted. Welcome back!")
                    print("✅ Authentication Successful!\n")
                    return True
                else:
                    attempts += 1
                    remaining = maxm_attempts - attempts
                    
                    if remaining > 0:
                        engine.say("Incorrect password.  attempts remaining.")
                        print(f"❌ Incorrect. {remaining} attempts left.\n")
                    else:
                        speak("Maximum attempts reached. Access denied.")
                        print("❌ Access Denied - Too many failed attempts.\n")
                        return False
                        
            except sr.UnknownValueError:
                print("❌ Could not understand. Please try again.")
                speak("I couldn't understand that. Please speak clearly.")
                attempts += 1
                
            except sr.RequestError:
                print(" Internet connection issue. Trying typed password...")
                speak("Voice authentication failed. You can type your password.")
                
                # Fallback to typed password
                typed_pass = input("Type password: ").strip().lower()
                if typed_pass == PASSWORD.lower():
                    speak("Access granted.")
                    print("✅ Authentication Successful!\n")
                    return True
                else:
                    attempts += 1
                    remaining = maxm_attempts - attempts
                    if remaining > 0:
                        speak(f"Incorrect. {remaining} attempts remaining.")
                    else:
                        speak("Access denied.")
                        return False
                        
            except Exception as e:
                print(f"Error: {e}")
                attempts += 1
    
    return False

def wish():
    hour = int(datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good morning sir, I am Visteeria your personalised AI assistant. How may I help you!")
    elif hour >= 12 and hour < 16:
        speak("Good afternoon sir, I am Visteeria your personalised AI assistant. How may I help you!")
    elif hour >= 16 and hour < 19:
        speak("Good evening sir, I am Visteeria your personalised AI assistant. How may I help you!")
    else:
        speak("Good night sir, I am Visteeria your personalised AI assistant. How may I help you!")

def takecommand():
    """Voice input function"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Visteeria is Listening...")
    
        r.pause_threshold = 1
        r.energy_threshold = 250
        try:
            r.adjust_for_ambient_noise(source, duration=1)
        except:
            pass
        audio = r.listen(source, timeout=4, phrase_time_limit=6)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"1234 said: {query}\n")
        return query
    except sr.UnknownValueError:
        print("Could not understand audio")
        return "None"
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        engine.say("There seems to be an internet issue.")
        return "None"
    except Exception as e:
        print(f"Error: {e}")
        speak("Something went wrong. Please try again.")
        return "None"

def write_command():
    """Text input function"""
    try:
        query = input("Type your command: ").strip()
        print(f"1234 typed: {query}\n")
        return query
    except Exception as e:
        print(f"Error reading input: {e}")
        return "None"

def get_input_mode():
    """Let user choose input method"""
    print("\n" + "="*50)
    print("Choose input mode:")
    print("1. Voice (speak)")
    print("2. Text (type)")
    print("3. Auto (voice by default, type 'switch' to go from text to voice command)")
    print("="*50)
    
    choice = input("Enter choice (1/2/3): ").strip()
    return choice

def process_command(query):
    """Process the user's command"""
    if query == "none" or not query:
        return True  
        
    print(f"Processing: {query}")
    
    # Wikipedia search
    if 'wikipedia' in query:
        try:
            engine.say("Searching Wikipedia...")
            search_query = query.replace("wikipedia", "").strip()
            print(f"Searching for: '{search_query}'")
            
            if not search_query:
                speak("What would you like me to search for on Wikipedia?")
                return True
                
            print("Fetching results...")
            results = wikipedia.summary(search_query, sentences=2)
            print(f"Results:\n{results}")
            engine.say("According to Wikipedia")
            speak(results)
            
        except wikipedia.exceptions.DisambiguationError as e:
            print(f"Multiple results found. Using: {e.options[0]}")
            results = wikipedia.summary(e.options[0], sentences=2)
            print(f"Results:\n{results}")
            speak(f"I found multiple results. Here's information about {e.options[0]}")
            speak(results)
            
        except wikipedia.exceptions.PageError:
            print("No Wikipedia page found")
            engine.say("Sorry, I couldn't find that page on Wikipedia.")
            
        except Exception as e:
            print(f"Wikipedia error: {e}")
            engine.say("Sorry, there was an error searching Wikipedia.")


    #  pre entered commands
    
    elif 'open youtube' in query:
        print("Opening YouTube...")
        engine.say("Opening YouTube")
        webbrowser.open("https://youtube.com")
        
    elif 'open whatsapp' in query:
        print("Opening WhatsApp...")
        engine.say("Opening WhatsApp")
        webbrowser.open("https://web.whatsapp.com/")


    

    elif 'open claude' in query:
        print("opening claude")
        engine.say("opening claude")
        webbrowser.open("https://claude.ai")
        
    elif 'weather' in query:
        print("fetching weather...")
        engine.say("opening weather forecast")
        webbrowser.open("https://zoom.earth.com")
        
    elif 'the time' in query:
        strtime = datetime.now().strftime("%H:%M:%S")
        print(f"Current time: {strtime}")
        engine.say("Sir, the time is")
        speak(strtime)

    elif 'what can you do' in query or 'your work' in query:
        response = "I can search Wikipedia, open YouTube and WhatsApp, tell you the time, search Google, and check weather. Just ask me!"
        speak(response)

    elif 'on youtube' in query and 'search' in query:
        search_term = query.replace('youtube', '').replace('search', '').strip()
        if search_term:
            engine.say(f"Searching YouTube for {search_term}")
            webbrowser.open(f"https://www.youtube.com/results?search_query={search_term}")

        else:
            speak("What would you like me to search for on YouTube?")


    elif 'search' in query or 'google' in query:
        search_term = query.replace('search', '').replace('google', '').strip()
        engine.say(f"Searching for {search_term}")
        webbrowser.open(f"https://www.google.com/search?q={search_term}")   

    elif 'linkedin' in query:
        engine.say("opening linkedin") 
        print("opening linkedin") 
        webbrowser.open("https://www.linkedin.com")

    elif 'github' in query:
        engine.say("opening github")                                          
        print("opening github") 
        webbrowser.open("https://github.com/")


    elif 'your name' in query:
        print("I am Visteeria")
        engine.say("I am Visteeria")


    elif 'how are you' in query:
        print("I am good")
        engine.say("I am good")


    

    #  asssistant band krne k
    elif any(word in query for word in ['exit', 'quit', 'enough', 'bye', 'stop']):
        print("Assistant shutting down...")
        
        return False  

        
    # Default response
    else:
        print("Command not recognized")
        engine.say("I didn't understand that command. Try asking me about Wikipedia, time, or to open YouTube or WhatsApp.")
    
    return True  # Continue loop


if __name__ == "__main__":
    print("="*60)
    print("🔐 VISTEERIA AI ASSISTANT - SECURE MODE")
    print("="*60)
    
    # Authenticate user first
    if not authenticate():
        print("\n❌ Authentication failed. Exiting...")
        speak("Security lockout activated. Goodbye.")
        exit()
    
    # If authenticated, proceed normally
    wish()
    print("Visteeria is ready! Say/Type 'exit' to quit.\n")
    
    mode = get_input_mode()
    use_voice = True
    
    while True:
        if mode == '1':
            query = takecommand().lower()
        elif mode == '2':
            query = write_command().lower()
        elif mode == '3':
            if use_voice:
                print("\n[Voice Mode] - Type 'switch' in next turn to use text")
                query = takecommand().lower()
            else:
                print("\n[Text Mode] - Type 'switch' to use voice")
                query = write_command().lower()
            
            if 'switch' in query:
                use_voice = not use_voice
                mode_name = "voice" if use_voice else "text"
                speak(f"Switching to {mode_name} mode")
                continue
        else:
            print("Invalid choice. Using voice mode.")
            query = takecommand().lower()
        
        should_continue = process_command(query)
        if not should_continue:
            break