import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import youtube_dl
import json

client = commands.Bot(command_prefix='!')

@client.event
async def on_ready():
    print('Bot connected to server!')


# Join/Leave a voice channel
@client.command(pass_context=True)
async def join(ctx):
    channel = ctx.message.author.voice.channel
    if channel.id != 901362479584645125:
        if ctx.author.voice:
            await channel.connect()
            await ctx.send(f'Bot connected to voice channel \"{channel}\" successfully!')
        else:
            await ctx.send('Please join a voice channel')
    else:
        await ctx.send('Bot is not allowed to join channel \'Discussion\'')


# -------------------Playing Audio from Youtube URL-------------------
@client.command()
async def play(ctx, url: str):
    ctx.voice_client.stop()
    FFMPEG_OPTIONS = {"before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5", "options": "-vn"}
    YDL_OPTIONS = {"format": "bestaudio"}
    vc = ctx.voice_client

    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['formats'][0]['url']
        source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
        vc.play(source)

@client.command()
async def pause(ctx):
    voice_client = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice_client.is_connected():
        voice_client.pause()
        await ctx.send('Audio Paused!')
    else:
        await ctx.send('The audio is not currently playing!')

@client.command()
async def resume(ctx):
    voice_client = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice_client.is_connected():
        voice_client.resume()
        await ctx.send('Audio Resumed!')
    else:
        await ctx.send('The audio is not currently paused!')

@client.command()
async def stop(ctx):
    voice_client = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice_client.stop()
    await ctx.send('Audio Stopped!')

# Handling Errors
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Invalid command')

@client.command(pass_context=True)
async def leave(ctx):
    if ctx.author.voice.channel and ctx.author.voice.channel == ctx.voice_client.channel:
        await ctx.voice_client.disconnect()
        await ctx.send('Bot successfully disconnected from the voice channel')


# Playlist
@client.command()
async def new_playlist(ctx, *, playlist_name):
    author = ctx.message.author
    guild = ctx.guild
    file = open(f'Playlists/{guild}/{author}/{playlist_name}.json')
    file.close()
    await ctx.send(f'New Playlist created \"{playlist_name}\"')

@client.command()
async def del_playlist(ctx, *, playlist_name):
    author = ctx.message.author
    with open(f'Playlists/{author}/{playlist_name}.json', encoding='utf-8'):
        os.remove(f"Playlists/{author}/{playlist_name}.json")

load_dotenv()
client.run(os.getenv('VOICE_BOT_TOKEN'))
