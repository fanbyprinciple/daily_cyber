import os
from dotenv import load_dotenv
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import MessageEmpty, MessageService, Channel
import csv

# Load environment variables from .env file
load_dotenv()

# Get API credentials from environment variables
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')

# Ensure credentials are loaded
if not api_id or not api_hash:
    raise ValueError("API_ID and API_HASH must be set in the .env file")

# Convert api_id to integer
try:
    api_id = int(api_id)
except ValueError:
    raise ValueError("API_ID in .env must be a valid integer")

# --- Telegram Client Setup ---
# You can choose a session name. This will create a .session file to store your login.
session_name = 'my_telegram_session'

client = TelegramClient(session_name, api_id, api_hash)

async def main():
    print("Connecting to Telegram...")
    await client.start()
    print("Client Connected!")

    # --- Find the target group ---
    group_name = 'Invest With Soumyadeep'
    target_group = None
    async for dialog in client.iter_dialogs():
        print(dialog.title)  # Debugging output
        # Check if it's a chat (group/channel) and if its title matches
        if dialog.is_channel and dialog.title == group_name:
            target_group = dialog.entity
            break
        elif dialog.is_group and dialog.title == group_name:
            target_group = dialog.entity
            break


    if target_group is None:
        print(f"Error: Group '{group_name}' not found. Make sure you are a member and the name is exact.")
        await client.disconnect()
        return

    print(f"Found group: {target_group.title} (ID: {target_group.id})")

    # --- Exporting chats ---
    print(f"Exporting messages from '{group_name}'...")
    all_messages = []
    offset_id = 0
    limit = 100 # Number of messages to fetch per request

    while True:
        history = await client(GetHistoryRequest(
            peer=target_group,
            offset_id=offset_id,
            offset_date=None,
            add_offset=0,
            limit=limit,
            max_id=0,
            min_id=0,
            hash=0
        ))
        messages = history.messages

        if not messages:
            break

        for message in messages:
            if isinstance(message, MessageEmpty) or isinstance(message, MessageService):
                continue # Skip empty or service messages

            # Extract relevant information
            msg_data = {
                'id': message.id,
                'date': message.date.isoformat(),
                'sender': '',
                'message': message.message,
                'views': message.views if hasattr(message, 'views') else None,
                'media_type': None
            }

            # Get sender information
            if message.sender:
                if hasattr(message.sender, 'first_name') and hasattr(message.sender, 'last_name'):
                    msg_data['sender'] = f"{message.sender.first_name or ''} {message.sender.last_name or ''}".strip()
                elif hasattr(message.sender, 'title'): # For channels
                    msg_data['sender'] = message.sender.title
                else:
                    msg_data['sender'] = f"User ID: {message.sender.id}"

            # Get media type
            if message.media:
                msg_data['media_type'] = type(message.media).__name__

            all_messages.append(msg_data)

        # Update offset_id for the next batch
        offset_id = messages[-1].id

        # To avoid rate limits, consider a small delay here if fetching a very large number of messages
        # import asyncio
        # await asyncio.sleep(0.5)

    print(f"Exported {len(all_messages)} messages.")

    # --- Save to CSV ---
    output_filename = f"{group_name}_chats.csv"
    if all_messages:
        keys = all_messages[0].keys()
        with open(output_filename, 'w', newline='', encoding='utf-8') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(all_messages)
        print(f"Messages saved to {output_filename}")
    else:
        print("No messages to save.")

    await client.disconnect()
    print("Client Disconnected.")

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())