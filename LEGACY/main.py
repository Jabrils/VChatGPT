import os
import json
from datetime import datetime
import openai
import argparse
import subprocess
import backend as b
from colorama import Fore, Style, init


def run_SATH_R(filename):
    try:
        subprocess.run(["python", "scripts/SATH-R.py", "--filename", filename], check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running grab3.py: {e}")

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

openai.api_key = key

prompt = args.prompt

# print("read file")

thread = []

# add the new message to the thread
thread.append({"role": "user", "content": prompt})

current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

print(f"\t{Fore.GREEN}Human [{current_datetime}]{Style.RESET_ALL}: {prompt}")

chat = openai.ChatCompletion.create(model='gpt-4', messages=thread)
reply = chat.choices[0].message.content

print("\n\n")

current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
# print(f'AI [{current_datetime}]: "{reply}"')
print(f'\t{Fore.RED}AI [{current_datetime}]{Style.RESET_ALL}: "{reply}"')

print("\n\n")
