# BotTest 0.0.1
# Author: Reannu Instrella
# Bookmark
from _thread            import start_new_thread 
import discord
import random
import os
from discord.ext import commands
import pyglet
import ui
import asyncio



#Command Prefix
intents = discord.Intents.all()
client = commands.Bot(command_prefix= ";", intents=intents)



#COMMANDS

@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

@client.command()
async def ping(ctx):
        await ctx.send(f'Pong!')

async def peng(ctx):
        await ctx.send(f'Pong!')

@client.command(aliases = ['maps','mappick'])
async def valmap(ctx):
    maps = ['Ascent', 'Icebox', 'Bind', 'Haven','Split']
    await ctx.send(f'Answer: {random.choice(maps)}')

@client.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)

@client.command()
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'Kicked {member.mention}')

@client.command()
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'Banned {member.mention}')

@client.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()

    member_name, member_discriminator = member.split("#")

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.member_discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return
    
    print(banned_users)

@client.command()
async def members(ctx):
    await ctx.channel.purge(limit=1)
    all_users = ctx.guild.members
    for member in all_users:
        print(member)



for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

#client.run('ODI0OTQ0MjEyNzUwODkzMDg2.YF2vKw.MNqL9rh4KR9FY6z4iuDG3BlmMTU') #BotTest
async def main():
    appwindow = ui.App()
    task2 = asyncio.create_task(client.run('ODI0OTE1MjE3NjYyMDgzMTIz.YF2UKg.0dzB4-urKJLJVwjqjKEzVTHq1NI'))
    task = asyncio.create_task(pyglet.app.run())
   
    
    await task2
    await task
    
asyncio.run(main())
 #BibiBot
