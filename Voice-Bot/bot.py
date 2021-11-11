import discord
from discord.ext import commands, tasks
import youtube_dl
from dotenv import load_dotenv
import os
import json

client = commands.Bot(command_prefix='!')

@client.event
async def on_ready():
    print('Bot connected to server!')

# Join/Leave a voice channel
@client.command(pass_context = True)
async def join(ctx):
    channel = ctx.message.author.voice.channel
    if (channel.id != 901362479584645125):
        if (ctx.author.voice):
            await channel.connect()
            await ctx.send(f'Bot connected to voice channel \"{channel}\" successfully!')
        else:
            await ctx.send('Please join a voice channel')
    else:
        await ctx.send('Bot is not allowed to join channel \'Discussion\'')

# -------------------Playing Audio from Youtube-------------------
players = {}
@client.command(pass_context = True)
async def play(ctx, url):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url)
    players[server.id] = player
    player.start()


# Handling Errors
# --------------------------------------------------------------
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Invalid command')
#  --------------------------------------------------------------

@client.command(pass_context = True)
async def leave(ctx):
     if (ctx.author.voice.channel and ctx.author.voice.channel == ctx.voice_client.channel):
        await ctx.voice_client.disconnect()
        await ctx.send('Bot successfully disconnected from the voice channel')

# Playlist
@client.command(pass_context = True)
async def playlist(ctx, *, playlist_name):
    with open(f'{playlist_name}.json', 'r') as f:
        data = json.load(f)
        await ctx.send(data)

@client.command(pass_context = True)
async def new_playlist(ctx, *, playlist_name):
    with open(f'{playlist_name}.json', 'w', encoding='utf-8') as json_playlist:
        await ctx.send(f'New playlist \"{playlist_name}\" created!')

# -----Adding new URLs to the playlist-------
@client.command(pass_context=True)
async def playlist_add(ctx, name, url):
    key = name
    value = url

load_dotenv()
client.run(os.getenv('VOICE_BOT_TOKEN'))
