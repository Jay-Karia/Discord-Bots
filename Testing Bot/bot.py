import discord
from discord.ext import commands
import random
import os
from dotenv import load_dotenv

client = commands.Bot(command_prefix='.')

@client.event
async def on_ready():
    print("Bot connected to server!")

@client.command()
async def ping(ctx):
    await ctx.channel.send('Pong!')

@client.command(aliases=['8Ball'])
async def _8ball(ctx, *, question):
    responses = ['It is certain',
                 'It is decidedly so',
                 'Without a doubt',
                 'Yes - definitely',
                 'You may rely on it',
                 'Better not tell you now',
                 'Ask again later',
                 'Cannot predict now',
                 'Concentrate and ask again',
                 'Reply hazy, try again',
                 'My reply is no',
                 'Don\'t count on it',
                 'My sources say no',
                 'Very doubtfull',
                 'Outlook not so good']
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

# Clear command
@client.command()
async def clear(ctx, amount=1):
    await ctx.channel.purge(limit = amount)

# Kick and Ban
@client.command()
async def kick(ctx, member : discord.Member, *,reason = None):
    await member.kick(reason=reason)
    await ctx.channel.send(f'@{member} was kicked by {client.user}')

@client.command()
async def ban(ctx, member : discord.Member, *,reason = None):
    await member.ban(reason=reason)
    await ctx.channel.send(f'@{member} was banned by {client.user}')

# Unban

load_dotenv()
client.run(os.getenv('TOKEN'))
