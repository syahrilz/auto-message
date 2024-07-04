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
    channel_id = "1242400774399725588"

    # Read the messages from "pesan.txt"
    with open("pesan.txt", "r", encoding="utf-8") as f:
        words = [line.strip() for line in f.readlines()]

    # Initialize the index to keep track of the current line
    index = 0

    # Variables to track the status of the last printed messages
    last_send_status = None
    last_delete_status = None

    # Loop to send messages every 5 seconds
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
                if last_send_status != 'success':
                    print(Fore.GREEN + "Success: Message sent successfully.")
                    last_send_status = 'success'
                message_id = r.json()['id']

                # Wait for 1 second before deleting the message
                time.sleep(0)

                # Delete the message
                delete_r = requests.delete(f"https://discord.com/api/v9/channels/{channel_id}/messages/{message_id}", headers=headers)

                if delete_r.status_code == 200:
                    if last_delete_status != 'success':
                        print(Fore.GREEN + "Success: Message deleted successfully.")
                        last_delete_status = 'success'
                else:
                    if last_delete_status != f'fail_{delete_r.status_code}':
                        print(Fore.RED + f"Error: Failed to delete message. Status code: {delete_r.status_code}")
                        last_delete_status = f'fail_{delete_r.status_code}'

            else:
                if last_send_status != f'fail_{r.status_code}':
                    print(Fore.RED + f"Error: Failed to send message. Status code: {r.status_code}")
                    last_send_status = f'fail_{r.status_code}'

            # Move to the next line
            index = (index + 1) % len(words)  # Loop back to the start when reaching the end

            # Wait for 5 seconds before sending the next message
            time.sleep(5)
        except Exception as e:
            if last_send_status != f'error_{e}':
                print(Fore.RED + f"Error: {e}")
                last_send_status = f'error_{e}'
            time.sleep(5)  # Wait a bit before retrying in case of error

# Run the message sending function
if __name__ == '__main__':
    send_messages()
