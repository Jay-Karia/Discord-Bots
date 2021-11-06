import discord
from discord.ext import commands, tasks
import random
import os
from discord.ext.commands.errors import CommandNotFound
from dotenv import load_dotenv
from itertools import cycle
import json

# Server Prefixes
def get_prefix(client, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    
    return prefixes[str(message.guild.id)]

client = commands.Bot(command_prefix=get_prefix)

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
# Checks
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount : int):
    await ctx.channel.purge(limit = amount)

# Kick and Ban
@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, *,reason = None):
    await member.kick(reason=reason)
    await ctx.channel.send(f'@{member} was kicked by {client.user}')

@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, *,reason = None):
    await member.ban(reason=reason)
    await ctx.channel.send(f'@{member} was banned by {client.user}')

@client.command()
async def info(ctx, *, botName):
    testing_bot_info = '''
    @Testing Bot 
⬇️ COMMANDS ⬇️
➡️  .ping --- reply "pong" 
➡️  .8Ball (question) -- reply a random answer to your question
➡️  .clear (number) -- clears the number of message given by the user
➡️  .change_status (status) -- will change the bot status 
➡️ .kick (member) (reason)-- will kick a member
➡️ .ban (member) (reason) -- will ban a member
➡️ .info (bot name) -- to display this message to any text channel
-------------------------------- 
⬇️ USES ⬇️
➡️ It is made for learning discord.py 
    '''
    if botName == 'Testing Bot':
        await ctx.send(testing_bot_info)

# Unban
@client.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_dis = member.split('#')

    for banned_entries in banned_users:
        user = banned_entries.user

        if (user.name, user.dis) == (member_name, member_dis):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return

# Bot Status
@client.command()
async def change_status(ctx, status):
    if status == 'online':
        await client.change_presence(status=discord.Status.online)
    if status == 'offline':
        await client.change_presence(status=discord.Status.offline)
    if status == 'dnd':
        await client.change_presence(status=discord.Status.dnd)
    if status == 'idle':
        await client.change_presence(status=discord.Status.idle)

    await ctx.send(f'Status Successfully changed to {status}!')

# Background Tasks
status = cycle(['Status 1', 'Status 2'])
@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))

# Errors
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Invalid Command Used!')

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please specify the amount of messages to be deleted.')

# Checks
def is_it_me(ctx):
    return ctx.author.id == 787915396569104384

@client.command()
@commands.check(is_it_me)
async def example(ctx):
    await ctx.send(f'Hi I\'m {ctx.author}')

load_dotenv()
client.run(os.getenv('TOKEN'))