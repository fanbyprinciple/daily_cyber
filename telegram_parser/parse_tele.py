from telethon.sync import TelegramClient
from telethon.errors.rpcerrorlist import SessionPasswordNeededError
from secrets import get_api_credentials

print (get_api_credentials())

api_id, api_hash, phone_number, session_name = get_api_credentials()

async def get_all_chats():
    """
    Connects to Telegram and retrieves all chats (dialogs).
    """
    # Create a new TelegramClient instance
    # The session_name.session file will be created to store your session
    async with TelegramClient(session_name, api_id, api_hash) as client:
        try:
            # Connect to Telegram
            if not await client.is_user_authorized():
                await client.send_code_request(phone_number)
                try:
                    await client.sign_in(phone_number, input('Enter the code you received: '))
                except SessionPasswordNeededError:
                    await client.sign_in(password=input('Enter your two-factor authentication password: '))

            print("Successfully connected to Telegram!")
            print("\nFetching all chats (dialogs)...")

            chats_count = 0
            async for dialog in client.iter_dialogs():
                chats_count += 1
                print(f"Chat Name: {dialog.name}, Chat ID: {dialog.id}")

            if chats_count == 0:
                print("No chats found.")
            else:
                print(f"\nFound {chats_count} chats.")

        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            # Ensure the client is disconnected when done or if an error occurs
            if client.is_connected():
                await client.disconnect()
                print("Disconnected from Telegram.")

async def get_specific_chat(chat_name):
    """
    Connects to Telegram and retrieves a specific chat by name.
    """
    # Create a new TelegramClient instance
    # The session_name.session file will be created to store your session
    async with TelegramClient(session_name, api_id, api_hash) as client:
        try:
            # Connect to Telegram
            if not await client.is_user_authorized():
                await client.send_code_request(phone_number)
                try:
                    await client.sign_in(phone_number, input('Enter the code you received: '))
                except SessionPasswordNeededError:
                    await client.sign_in(password=input('Enter your two-factor authentication password: '))

            print("Successfully connected to Telegram!")
            print("\nFetching all chats (dialogs)...")

            chats_count = 0
            async for dialog in client.iter_dialogs():
                chats_count += 1
                print(f"Chat Name: {dialog.name}, Chat ID: {dialog.id}")

            if chats_count == 0:
                print("No chats found.")
            else:
                print(f"\nFound {chats_count} chats.")

        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            # Ensure the client is disconnected when done or if an error occurs
            if client.is_connected():
                await client.disconnect()
                print("Disconnected from Telegram.")

if __name__ == '__main__':
    import asyncio
    # On Windows, you might need to set a different event loop policy
    # if you encounter issues with the default one.
    # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(get_all_chats())