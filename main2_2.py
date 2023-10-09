
import speech_recognition as sr

def listen():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Please speak something...")
        audio_data = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio_data)
            print("You said:", text)
            return text
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
    if user_input.lower() in ["exit", "quit"]:
        break  # Exit the loop if the user types "exit" or "quit"
    
    print("\n")
    # add the new message to the thread
    thread.append({"role": "user", "content": user_input})

    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # print(f"\t{Fore.GREEN}Human [{current_datetime}]{Style.RESET_ALL}: {user_input}")

    chat = openai.ChatCompletion.create(model='gpt-4', messages=thread)
    reply = chat.choices[0].message.content

    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    print(f'\t{Fore.RED}AI [{current_datetime}]{Style.RESET_ALL}: "{reply}"')

    # add the AI's reply to the thread
    thread.append({"role": "system", "content": reply})

    print("\n")
