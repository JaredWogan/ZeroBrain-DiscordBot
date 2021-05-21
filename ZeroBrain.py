# Zero Brain - The Discord Bot
# Created by Jared Wogan
# Version 0.1

import asyncio
import os
import random

import discord
from discord.ext import tasks
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents().all()
intents.members = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

    channel_general_id = await getChannelGeneral()
    print('The General channel has ID:', channel_general_id)

    guild = discord.utils.get(client.guilds, name=GUILD)
    members_data = [member for member in guild.members]
    members = [[member.name.encode('cp850', errors='replace').decode('cp850'), member.id] for member in members_data]
    print('Members:\n', '-', '\n - '.join(['Name: ' + member[0] + ' - ID: ' + str(member[1]) for member in members]))

    drink.start(channel_general_id)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    response = 'Zach Fat!'
    await message.channel.send(response)

    # if message.content == '':
    #     response = 'Zach Fat!'
    #     await message.channel.send(response)

    if message.content == 'shutdown':
        exit()


@tasks.loop(seconds=30)
async def drink(channel_id):
    msg_channel = client.get_channel(channel_id)
    while True:
        sleepTimer = random.randint(3600, 14400)
        print(
            'Sending drink reminder in',
            sleepTimer // 3600,
            'hour(s)',
            sleepTimer % 3600 // 60,
            'minute(s) and',
            (sleepTimer - 3600 * (sleepTimer // 3600) - 60 * (sleepTimer % 3600 // 60)),
            'seconds'
        )
        await asyncio.sleep(sleepTimer)
        await msg_channel.send('🍻 Finish your drink 🍻')


async def getChannelGeneral():
    guild = discord.utils.get(client.guilds, name=GUILD)
    channels = [channel for channel in guild.text_channels]
    channel_general_ids = [channel.id for channel in channels if 'general' in channel.name]
    return channel_general_ids[0]

client.run(TOKEN)
