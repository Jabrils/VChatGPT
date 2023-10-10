

import pyttsx3

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    
import speech_recognition as sr

def listen():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Please speak something...")
        audio_data = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio_data)
            print(f"\t{Fore.GREEN}You{Style.RESET_ALL}:", text)

            if "chai" in text.lower():
                return text.split('chai')[1]
            else:
                return None
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            return None
    
import os
import json
from datetime import datetime
import openai
import argparse
import subprocess
import backend as b  # Assuming this is a module you have
from colorama import Fore, Style, init

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

while True:  # Keep the conversation going until the user decides to exit
    user_input = listen()
    if user_input is None:
        print("Didn't catch that. Trying again.")
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
