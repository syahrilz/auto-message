import requests
import time
import os
from colorama import Fore, init
from dotenv import load_dotenv

# Initialize colorama
init(strip=True)

# Load environment variables from .env file if running locally
load_dotenv()

# Get the authorization token from environment variables
authorization = os.getenv("TOKEN")

def send_messages():
    # Set the channel ID where messages will be sent
    channel_id = "1236271755576872991"

    # Read the messages from "pesan.txt"
    with open("pesan.txt", "r", encoding="utf-8") as f:
        words = [line.strip() for line in f.readlines()]

    # Initialize the index to keep track of the current line
    index = 0

    # Loop to send messages every 120 seconds
    while True:
        try:
            payload = {
                'content': words[index]
            }

            headers = {
                'Authorization': authorization
            }

            # Send the message
            r = requests.post(f"https://discord.com/api/v9/channels/{channel_id}/messages", data=payload, headers=headers)

            # Check if message sent successfully
            if r.status_code == 200:
                print(Fore.GREEN + "Success: Message sent successfully.")
            else:
                print(Fore.RED + f"Error: Failed to send message. Status code: {r.status_code}")

            # Move to the next line
            index = (index + 1) % len(words)  # Loop back to the start when reaching the end

            # Wait for 100 seconds before sending the next message
            time.sleep(100)
        except Exception as e:
            print(Fore.RED + f"Error: {e}")
            time.sleep(5)  # Wait a bit before retrying in case of error

# Run the message sending function
if __name__ == '__main__':
    send_messages()
