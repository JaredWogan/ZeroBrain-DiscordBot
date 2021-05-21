# Zero Brain - The Discord Bot
# Created by Jared Wogan
# Version 0.1

import asyncio
import os
import random
import wikipedia

import discord
from discord.ext import tasks
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents().all()
intents.members = True
client = discord.Client(intents=intents)

zach_id = 0


@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

    guild = discord.utils.get(client.guilds, name=GUILD)
    members_data = [member for member in guild.members]
    members = [
        [member.name.encode('cp850', errors='replace').decode('cp850'), member.id,
         nicknames(member.nick), voice(member)]
        for member in members_data
    ]
    users_info = [
        'Name: ' + member[0] + ' - ID: ' + str(member[1]) + ' - Nick: ' + member[2] + ' - Channel: ' + member[3]
        for member in members
    ]
    print('Members:\n', '-', '\n - '.join(users_info))

    zachs = [member for member in members_data if 'Zach' in nicknames(member.nick)]
    zach = zachs[0]

    drink.start(getChannelGeneral())
    zachFat.start(getChannelGeneral(), zach)
    random_page.start(getChannelGeneral())


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == 'shutdown':
        exit()

    if 'http' not in message.content and '!clear' not in message.content:
        with open('Markov.txt', 'a', encoding='utf-8') as file:
            file.write(str(message.content).encode('cp850', errors='replace').decode('cp850') + '\n')

    messages = [
        '(⓿_⓿)',
        'w(ﾟДﾟ)w',
        '(╯‵□′)╯︵┻━┻',
        'https://tenor.com/view/blank-stare-really-i-dont-believe-you-side-eye-looking-gif-6151149',
        'https://tenor.com/view/thomas-the-tank-engine-shocked-surprised-woah-what-gif-5667771'
    ]
    chance = 5
    if message.channel.id == getChannelGeneral():
        if random.randint(0, 100) <= chance:
            response = random.choice(messages)
            await message.channel.send(response)


@tasks.loop(seconds=30)
async def zachFat(channel_id, zach):
    msg_channel = client.get_channel(channel_id)
    zach_connected = [True if voice(zach) != 'Not Connected' else False, False]
    while True:
        if zach_connected[0] and not zach_connected[1]:
            await msg_channel.send(f'<@{zach.id}> Zach Fat ')
        zach_connected = [True if voice(zach) != 'Not Connected' else False, zach_connected[0]]
        await asyncio.sleep(1)


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


@tasks.loop(seconds=30)
async def random_page(channel_id):
    msg_channel = client.get_channel(channel_id)
    while True:
        sleepTimer = random.randint(6000, 43200)
        print(
            'Sending Wikipedia fact in',
            sleepTimer // 3600,
            'hour(s)',
            sleepTimer % 3600 // 60,
            'minute(s) and',
            (sleepTimer - 3600 * (sleepTimer // 3600) - 60 * (sleepTimer % 3600 // 60)),
            'seconds'
        )
        await asyncio.sleep(sleepTimer)
        random_page = wikipedia.random(1)
        try:
            result = wikipedia.page(random_page).summary
            await msg_channel.send(result)
        except wikipedia.exceptions.DisambiguationError:
            print('Wikipedia Error')


def getChannelGeneral():
    guild = discord.utils.get(client.guilds, name=GUILD)
    channels = [channel for channel in guild.text_channels]
    channel_general_ids = [channel.id for channel in channels if 'general' in channel.name]
    return channel_general_ids[0]


def voice(member):
    if member is None:
        return 'Error'
    if member.voice is None:
        return 'Not Connected'
    else:
        return str(member.voice.channel).encode('cp850', errors='replace').decode('cp850')


def nicknames(nickname):
    if nickname is None:
        return 'No Nickname'
    else:
        return str(nickname)


client.run(TOKEN)
