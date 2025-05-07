# Import necessary libraries
import time
import random
import pyttsx3
import subprocess # <-- To run external processes (like opening apps)
import platform   # <-- To check OS type

# --- Initialize Text-to-Speech Engine ---
tts_engine = None
try:
    tts_engine = pyttsx3.init()
    # Optional: Configure voice, rate, volume
    print("TTS Engine Initialized successfully.")
except Exception as e:
    print(f"CRITICAL ERROR: Failed to initialize text-to-speech engine: {e}")
    print("Stark will only respond with speechrecoginition.")

# --- Define Stark's Identity ---
ai_name = "Stark"
current_os = platform.system().lower() # Get OS name ('windows', 'darwin' for macos, 'linux')

# --- Pre-defined Responses ---
# (Keep existing response lists: confirmation_phrases, unknown_responses, etc.)
confirmation_phrases = ["Acknowledged.", "Understood.", "Processing.", "On it.", "Noted.", "Affirmative."]
unknown_responses = ["I do not have parameters for that request.", "Unable to compute. Please rephrase.", "That query is outside my current operational directives.", "Request unclear.", "Cannot parse instruction."]
exit_phrases = ["Deactivating systems. Farewell.", "Stark signing off.", "Mission complete. Shutting down."]
greeting_responses = ["Greetings. Stark ready.", f"Hello. {ai_name} reporting.", f"{ai_name} online. How can I assist?"]
opening_app_responses = ["Executing command.", "Launching application now.", "Opening it for you."]
open_fail_responses = ["Sorry, I encountered an error trying to open that.", "Unable to launch the specified application.", "Command execution failed."]


# --- Helper Function to Speak ---
def speak(text_to_speak, delay_after=0.1):
    """Prints the text and speaks it using the TTS engine (if available)."""
    print(f"{ai_name}: {text_to_speak}")
    if tts_engine:
        try:
            tts_engine.say(text_to_speak)
            tts_engine.runAndWait()
            time.sleep(delay_after)
        except Exception as e:
            print(f"[TTS Error: Could not speak - {e}]")
    else:
        time.sleep(0.5)

# --- OS Interaction Function (Example: Open App) ---
def open_application(app_name_or_command):
    """Attempts to open a specified application using OS-specific commands."""
    speak(random.choice(opening_app_responses))
    try:
        if current_os == "windows":
            # For Windows, 'start' command usually works well
            subprocess.Popen(f'start {app_name_or_command}', shell=True)
            # NOTE: Using shell=True has security risks if app_name_or_command comes from untrusted input.
            # Since we hardcode the commands triggered by keywords below, it's *relatively* safer here.
            # Alternatives for specific apps: subprocess.Popen(['notepad.exe']) etc.
        elif current_os == "darwin": # MacOS
            subprocess.Popen(['open', '-a', app_name_or_command])
        elif current_os == "linux":
            # Linux can be tricky, depends on desktop environment. 'xdg-open' is common.
            subprocess.Popen([app_name_or_command]) # Try running directly
            # Or try: subprocess.Popen(['xdg-open', app_name_or_command])
        else:
             speak(f"Sorry, I don't have specific instructions to open apps on {current_os}.")
             return False # Indicate failure

        time.sleep(1) # Give the OS a moment to launch
        return True # Indicate success

    except FileNotFoundError:
         speak(f"Error: Command or application '{app_name_or_command}' not found.")
         return False
    except Exception as e:
         speak(f"{random.choice(open_fail_responses)} Error: {e}")
         return False


# --- Function for Stark's Startup Sequence ---
def stark_initialize():
    """Prints and speaks the initial activation message for Stark."""
    startup_message_1 = f"Initializing {ai_name} AI Core..."
    startup_message_2 = "Stark Systems Booting..."
    print(startup_message_1)
    time.sleep(1.0)
    print(startup_message_2)
    if tts_engine:
        speak(startup_message_1, delay_after=0)
        speak(startup_message_2, delay_after=0.5)
    else:
        time.sleep(1.5)

    print("...")
    time.sleep(0.5)
    print("="*30)
    print(f"** {ai_name.upper()} AI ONLINE **")
    print("="*30)
    time.sleep(0.5)

    speak(f"Operating System detected: {platform.system()}") # Announce OS
    speak("All systems nominal. Ready for input.")
    speak(f"You may address me as {ai_name}.")
    speak(" hiii sir")
    speak("welcome to mark 42")
    speak("i am at your service")
# --- Main Interaction Loop ---
def run_stark_interface():
    stark_initialize()

    while True:
        try:
            user_command = input("You: ")
            user_command_lower = user_command.lower().strip()

            if not user_command_lower:
                speak("Please provide a directive.")
                continue

            response = None
            action_taken = False # Flag to see if a specific action was handled

            # === Command Processing Logic ===

            # 1. Exit Commands (Highest Priority)
            exit_keywords = ["shutdown", "exit", "quit", "deactivate", "goodbye", "power off"]
            if any(keyword in user_command_lower for keyword in exit_keywords):
                response = random.choice(exit_phrases)
                speak(response)
                action_taken = True
                break # Exit loop immediately

            # 2. NEW: Open Application Commands
            # NOTE: Be specific with keywords to avoid accidental triggering
            if not action_taken:
                app_to_open = None
                if "open notepad" in user_command_lower:
                    app_to_open = "notepad" if current_os == "windows" else "TextEdit" if current_os == "darwin" else "gedit" # Example Linux editor
                elif "open calculator" in user_command_lower:
                     app_to_open = "calc" if current_os == "windows" else "Calculator" if current_os == "darwin" else "gnome-calculator" # Example Linux calc
                elif "launch chrome" in user_command_lower or "open chrome" in user_command_lower:
                     app_to_open = "chrome" if current_os == "windows" else "Google Chrome" if current_os == "darwin" else "google-chrome"
                elif "launch browser" in user_command_lower or "open browser" in user_command_lower:
                    # Example: Opens default browser. Might vary.
                    if current_os == "windows": app_to_open = "start" # Generic command
                    elif current_os == "darwin": app_to_open = "/Applications/Safari.app" # Opens Safari specifically, safer than just 'open' potentially
                    else: app_to_open = "xdg-open" # Requires a URL, might be better to open a specific browser like chrome/firefox


                # If an app was identified, try to open it
                if app_to_open:
                     success = open_application(app_to_open)
                     # No further 'response' needed here, open_application handles feedback
                     action_taken = True # Mark that we handled this command


            # 3. Greetings
            greeting_keywords = ["hello", "hi", "hey", "greetings"]
            if not action_taken and any(keyword in user_command_lower for keyword in greeting_keywords):
                 response = random.choice(greeting_responses)
                 action_taken = True

            # 4. Identity Check
            identity_keywords = ["who are you", "your name"]
            if not action_taken and any(keyword in user_command_lower for keyword in identity_keywords):
                 response = f"I am {ai_name}, your personal AI assistant."
                 action_taken = True
            
            # 4. Identity Check
            identity_keywords = ["access to os", "i am onit"]
            if not action_taken and any(keyword in user_command_lower for keyword in identity_keywords):
                 response = f"I am {ai_name}, your personal AI assistant."
                 action_taken = True
                 
            # 5. Default / Acknowledgment / Unknown
            if not action_taken: # If no specific action or response was triggered yet
                if random.random() < 0.8:
                    confirmation = random.choice(confirmation_phrases)
                    response = f"{confirmation} Command noted: '{user_command}'. Ready for next input."
                else:
                    response = random.choice(unknown_responses)

            # --- Speak the Response (if one was generated) ---
            if response:
                 speak(response)


        except (KeyboardInterrupt, EOFError):
            speak(f"Emergency shutdown detected. {random.choice(exit_phrases)}")
            break
        except Exception as e: # Generic catch-all for other unexpected errors
            print(f"\n--- UNEXPECTED ERROR ---")
            print(f"An error occurred: {e}")
            speak("Apologies. I've encountered an unexpected system error. Please check the console.")
            time.sleep(2)


    # --- Cleanup before exiting ---
    print("\nStark AI process terminating.")
    if tts_engine:
        try: tts_engine.stop()
        except Exception as e: print(f"[TTS Cleanup Error: {e}]")


# --- Run the AI ---
if __name__ == "__main__":
    run_stark_interface()