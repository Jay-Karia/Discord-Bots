import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

client = commands.Bot(command_prefix='!')

@client.event
async def on_ready():
    print('Bot connected to server!')

@client.command()
async def join(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        await channel.connect()
        await ctx.send('Bot successfully connected to voice channel')
    else:
        await ctx.send('Please join a voice channel!')

@client.command()
async def leave(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send('Bot successfully disconnected from the voice channel')
    else:
        await ctx.send('Bot is not currently in the voice channel')

load_dotenv()
client.run(os.getenv('TOKEN'))