import os
from client import RiotClient
from dotenv import load_dotenv
from helper import rank_data_by_queue_type, display_ranked_data
from random import choice
from typing import Final

load_dotenv()
KEY: Final[str] = os.getenv('API_KEY')

def get_ranked_response(args: list) -> str:
    username, tag = args[0].split('#')
    riot_client = RiotClient(KEY)
    puuid = riot_client.get_puuid_from_username_and_tagline(username, tag)
    summoner_data = riot_client.get_summoner_data(puuid)
    ranked_data = riot_client.get_rank_data(summoner_data.get('id'))
    message_strings = display_ranked_data(username, tag, rank_data_by_queue_type(ranked_data))
    return '\n'.join(message_strings)

def empty(args: list) -> str:
    return 'Well, you\'re awfully silent...'

def hello_there(args: list) -> str:
    return 'Hello there!'

def help(args: list) -> str:
    return 'try $commands'

def commands(args: list) -> str:
    command_list = [
        'Commands List:',
        '$hello',
        '$league username#hashtag',
        '$commands',
        '$help',
    ]
    return '\n'.join(command_list)



commands = {
    'league': get_ranked_response,
    'hello': hello_there,
    'help': help,
    'commands': commands,
    '': empty
}

def get_response(user_input: str) -> str:
    if user_input == '':
        return commands.get('')()

    command = user_input.split()[0]
    args = user_input.split()[1:]

    if not commands.get(command.lower()):
        return choice(['I do not understand...',
            'What are you talking about?',
            'Do you mind rephrasing that?'])

    return commands.get(command)(args)
