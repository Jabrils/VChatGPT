import pygame
import pyttsx3
import speech_recognition as sr
import openai
import threading
import random
import sys
import pyttsx3
import speech_recognition as sr
import os
import json
from datetime import datetime
import argparse
import subprocess
import backend as b  # Assuming this is a module you have
from colorama import Fore, Style, init
# ... (rest of your imports)

running = True

def display_image(image_path_open, image_path_closed):
    global running  # Access the global running flag
    # Initialize Pygame
    pygame.init()

    # Set the dimensions of the window
    window_size = (480, 800)
    screen = pygame.display.set_mode(window_size, pygame.NOFRAME)

    # Load the images
    image_open = pygame.image.load(image_path_open)
    image_closed = pygame.image.load(image_path_closed)

    # Start with eyes open
    current_image = image_open

    # Create a clock object to manage time
    clock = pygame.time.Clock()

    # Set the initial next blink time
    next_blink_time = pygame.time.get_ticks() + random.randint(2000, 5000)  # 2 to 5 seconds

    # Wait for user to quit
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    break

        current_time = pygame.time.get_ticks()
        if current_time >= next_blink_time:
            current_image = image_closed  # Close eyes
            screen.blit(current_image, (0, 0))
            pygame.display.flip()

            next_blink_time = current_time + random.randint(50, 150)  # 0.1 to 0.5 seconds

            while pygame.time.get_ticks() < next_blink_time:
                pass  # Busy wait (this can be replaced with other processing)

            current_image = image_open  # Open eyes
            next_blink_time = current_time + random.randint(2000, 5000)  # 2 to 5 seconds

        # Blit the current image and update the display
        screen.blit(current_image, (0, 0))
        pygame.display.flip()

        # Limit the frame rate to reduce CPU usage
        clock.tick(60)  # 60 frames per second

    # Quit Pygame
    running = False
    pygame.quit()
    sys.exit()

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def listen():
    global running  # Access the global running flag
    while running:
        recognizer = sr.Recognizer()

        with sr.Microphone() as source:
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

    while running:  # Keep the conversation going until the user decides to exit
        user_input = listen()
        if user_input is None:
            print("Didn't catch that. Trying again.")
            continue  # This will jump back to the start of the while loop
        elif user_input is "~":
            print("You weren't talking to me so ill ignore that.")
            continue  # This will jump back to the start of the while loop
        if user_input.lower() in ["exit", "quit"]:
            break
        
        print("\n")
        # add the new message to the thread
        thread.append({"role": "user", "content": user_input})

        current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        chat = openai.ChatCompletion.create(model='gpt-4', messages=thread)
        reply = chat.choices[0].message.content
        
        current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        print(f'\t{Fore.RED}AI [{current_datetime}]{Style.RESET_ALL}: "{reply}"')

        # Using Text To Speech to read the reply out loud
        speak(reply)

        # add the AI's reply to the thread
        thread.append({"role": "system", "content": reply})

        print("\n")

def main():
    global running  # Access the global running flag
    while running:
        image_path_open = 'Chai Faces/Smile.png'
        image_path_closed = 'Chai Faces/Blink.png'
        
        # Create threads for image display and conversation handling
        display_thread = threading.Thread(target=display_image, args=(image_path_open, image_path_closed))
        conversation_thread = threading.Thread(target=handle_conversation)
        
        # Start the threads
        display_thread.start()
        conversation_thread.start()
        
        # Wait for both threads to finish (this will block indefinitely in this example)
        display_thread.join()
        conversation_thread.join()

if __name__ == "__main__":
    main()
