# This example requires the 'message_content' intent.

import discord
import logging

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    # We don't want to react to messages from ourselves
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

handler = logging.FileHandler(filename='logs/discord.log', encoding='utf-8', mode='w')

import json

with open('config.json', 'r') as f:
    config = json.load(f)
    token = config['token']

client.run(token, log_handler=handler, log_level=logging.DEBUG)
