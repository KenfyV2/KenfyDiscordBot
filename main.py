from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from commands import get_response

# Load env
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

# Bot setup
intent: Intents = Intents.default()
intent.message_content = True
client: Client = Client(intents=intent)

# Message Functionality
async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print('(Message was empty because intents were not enabled probably)')
        return

    if is_private := user_message[0] == '?':
        user_message = user_message[1:]

    if is_public := user_message[0] == '$':
            user_message = user_message[1:]

    try:
        response: str = get_response(user_message)
        if is_private:
            await message.author.send(response) 
        elif is_public:
            await message.channel.send(response)
    except Exception as e:
        print(e)

# Handling Start Up

@client.event
async def on_ready() -> None:
    print(f'{client.user} is now runnning!')

# Handling Incoming Messages
@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return

    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)

    print(f'[{channel}] {username}: "{user_message}"')
    await send_message(message, user_message)

# Main entry path
def main() -> None:
    client.run(token=TOKEN)

if __name__ == '__main__':
    main()
