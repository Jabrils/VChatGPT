import pygame
import pyttsx3
import speech_recognition as sr
import openai
import threading
import random
import sys
import pyttsx3
import os
import json
from datetime import datetime
import argparse
import subprocess
import backend as b  # Assuming this is a module you have
from colorama import Fore, Style, init
import simpleaudio as sa
import re
# ... (rest of your imports)

running = True
state = "smile"
voice = []
order = 0

def run_piper(text):
    global state
    global order

    split_text = re.split(r'[.!?,";:]', text)
    # print(split_text)
    for t in split_text:
        padded_number = "{:04}".format(order)  # Pads with zeros to a width of 4

        # 
        with open(f'/tmp/fifos/piper_fifo_{padded_number}', 'w') as fifo:
            fifo.write(t)
        order+=1

    # state = "talking"

def monitor_audio_state():
    global running  # Access the global running flag
    global state
    global voice
    
    while running:  # Assuming `running` is a flag you use to control your threads
        path_To = "/tmp/wavs"

        # 
        if os.listdir(path_To):
            files = [os.path.join(path_To, file) for file in os.listdir(path_To)]
            voice = list(set(voice + files))
            print("VOICE CONFIRM:", voice)

        # 
        play_audio_queue()
        
def play_audio_queue():
    global voice
    global state

    try:
        while voice:  # Continue until the voice list is empty
            wav_path = voice[0]  # Get the first path in the list

            # if 
            if os.path.getsize(wav_path) > 0:
                wave_obj = sa.WaveObject.from_wave_file(wav_path)
                play_obj = wave_obj.play()
                state = "talking"
                play_obj.wait_done()  # Wait for the audio to finish playing
                state = "smile"
                os.remove(voice[0]) # delete it
                voice.pop(0)  # Remove the path from the list
    except Exception as e:
        print(f"Exception: {e}")
        print(f"E type: {type(e)}")

def display_image(image_path_smile, image_path_blinking, image_path_talking, image_path_thinking, image_path_listening):
    global running  # Access the global running flag
    global state
    # Initialize Pygame
    pygame.init()

    # Set the dimensions of the window
    window_size = (480, 800)
    screen = pygame.display.set_mode(window_size, pygame.NOFRAME)

    # Load the images
    image_smile = pygame.image.load(image_path_smile)
    image_blinking = pygame.image.load(image_path_blinking)
    image_talking = pygame.image.load(image_path_talking)
    image_thinking = pygame.image.load(image_path_thinking)
    image_listening = pygame.image.load(image_path_listening)

    # Start with eyes open
    current_image = image_smile

    # Create a clock object to manage time
    clock = pygame.time.Clock()

    # Set the initial next blink time
    next_blink_time = pygame.time.get_ticks() + random.randint(2000, 5000)  # 2 to 5 seconds
    next_talk_time = 0

    # Wait for user to quit
    running = True
    talk_state = True

    while running:
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        break

            current_time = pygame.time.get_ticks()

            #
            # match state:
            if state is "talking":
                if current_time >= next_talk_time:
                    if talk_state:
                        current_image = image_smile
                        talk_state = False
                    else:
                        current_image = image_talking
                        talk_state = True
                    next_talk_time = current_time + 75  # Set next change time to 1 second later
            elif state is "thinking":
                current_image = image_thinking
            elif state is "listening":
                current_image = image_listening
            elif state is "smile":
                if current_time >= next_blink_time:
                    current_image = image_blinking  # Close eyes
                    screen.blit(current_image, (0, 0))
                    pygame.display.flip()

                    next_blink_time = current_time + random.randint(50, 150)  # 0.1 to 0.5 seconds

                    while pygame.time.get_ticks() < next_blink_time:
                        pass  # Busy wait (this can be replaced with other processing)

                    current_image = image_smile  # Open eyes
                    next_blink_time = current_time + random.randint(2000, 5000)  # 2 to 5 seconds

            # Blit the current image and update the display
            screen.blit(current_image, (0, 0))
            pygame.display.flip()

            # Limit the frame rate to reduce CPU usage
            clock.tick(60)  # 60 frames per second
        except Exception as e:
            print(f"Exception: {e}")

    # Quit Pygame
    running = False
    pygame.quit()
    sys.exit()

def speak(text):
    global state
    engine = pyttsx3.init()
    engine.say(text)
    state = "talking"
    engine.runAndWait()
    state = "smile"

def listen():
    global running  # Access the global running flag
    global state
    while running:
        recognizer = sr.Recognizer()

        with sr.Microphone() as source:
            state = "smile"
            print("Please speak something...")
            audio_data = recognizer.listen(source)
            print("Trying to understand...")
            try:
                text = recognizer.recognize_google(audio_data)
                print(f"\t{Fore.GREEN}You{Style.RESET_ALL}:", text)

                if "chai" in text.lower():
                    return text.split('chai')[1]
                else:
                    return "~"
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
                return None

def handle_conversation():
    global running  # Access the global running flag
    global state
    # Initialize colorama
    init()

    # Set up argparse
    parser = argparse.ArgumentParser(description='OpenAI Chat Completion Script')
    parser.add_argument('--prompt', '-p', type=str, default="",
                        help='The human prompt for the chat')
    parser.add_argument('-G', '--generate', action='store_true', help='Start to generate this episode.')
    parser.add_argument('--cred', '-c', type=int, default=0, help='which creditials do you want to use')
    args = parser.parse_args()

    key = open("gpt-4", "r").read().strip('\n')
    print("\n")

    openai.api_key = key

    thread = []
    thread.append({"role": "system", "content": "Pretend you are a human named Chai having dynamic human conversations, so use words like 'I' & 'my' to sound more human. All all of your text will be read using TTS. Please keep your anwsers relatively brief unless asked to expand upon, & also please understand all text input will be Speech To Text, so there will be a few typos. Optimize your speaking patterns as if you are having a natural vocal conversation & NEVER say 'As an AI...'"})

    while running:  # Keep the conversation going until the user decides to exit
        try:
            user_input = listen()
            state = "listening"
            if user_input is None:
                print("Didn't catch that. Trying again.")
                continue  # This will jump back to the start of the while loop
            elif user_input is "~":
                print("You weren't talking to me so ill ignore that.")
                continue  # This will jump back to the start of the while loop
            if user_input.lower() in ["exit", "quit"]:
                break

            state = "thinking"

            print("\n")
            # add the new message to the thread
            thread.append({"role": "user", "content": user_input})

            current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

            chat = openai.ChatCompletion.create(model='gpt-4', messages=thread)
            reply = chat.choices[0].message.content

            current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            print(f'\t{Fore.RED}AI [{current_datetime}]{Style.RESET_ALL}: "{reply}"')

            # Using Text To Speech to read the reply out loud
            run_piper(reply)

            # add the AI's reply to the thread
            thread.append({"role": "system", "content": reply})
            
            #monitor_audio_state()
            print("\n")
        except Exception as e:
            print(f"Exception: {e}")

def create_directories():
    dirs_to_create = ["/tmp/fifos", "/tmp/wavs"]
    for dir_path in dirs_to_create:
        os.makedirs(dir_path, exist_ok=True)

def main():
    global running  # Access the global running flag
    create_directories()
    
    # Start the Bash script
    #bash_script_process = subprocess.Popen(['./piper_backend3.sh'])
    speak("startup activated")
    
    while running:
        image_path_smile = './Chai Faces/Smile.png'
        image_path_blink = 'Chai Faces/Blink.png'
        image_path_talking = 'Chai Faces/Talking.png'
        image_path_thinking = 'Chai Faces/Thinking.png'
        image_path_listening = 'Chai Faces/Listening.png'

        # Create threads for image display and conversation handling
        display_thread = threading.Thread(target=display_image, args=(image_path_smile, image_path_blink, image_path_talking, image_path_thinking, image_path_listening))
        conversation_thread = threading.Thread(target=handle_conversation)
        audio_monitor_thread = threading.Thread(target=monitor_audio_state)

        # Start the threads
        display_thread.start()
        conversation_thread.start()
        audio_monitor_thread.start()
        
        # Wait for both threads to finish (this will block indefinitely in this example)
        display_thread.join()
        conversation_thread.join()
        audio_monitor_thread.join()

if __name__ == "__main__":
    main()
