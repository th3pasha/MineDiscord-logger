import discord
from discord.ext import tasks
import asyncio

intents = discord.Intents.default()
intents.message_content = True


commandPrefix = '/'
command = 'minecraft'
token = 'MTA3ODA3NjMzMTg1NTcyODgwMA.G-qlre.xVYtjK9AGHTqjzvz1OvroRLccw3nDbqck9K3CU'

bot = discord.Client(intents=intents)

def filter_line(string):
    for line in string.split("\n"):
        if '[Server thread/WARN]' in line:
            continue
        if 'logged in with entity id' in line:
            continue
        if 'Disconnecting' in line:
            continue
        if 'Disconnected' in line:
            continue
        if '[Not Secure]' in line:
            continue
        if 'Timed out' in line:
            continue
        if 'com.mojang.authlib.GameProfile' in line:
            continue
        if '\n' in line:
            continue
        else:
            return line.replace("[Server thread/INFO]", "") + '\n'

def read_file(fileName):
    fileContent = ''
    with open(fileName, 'r') as f:
        file_lines = f.readlines()
        for line in file_lines:
            if(filter_line(line).isspace()):
                continue
            else:
                fileContent += filter_line(line)
    return fileContent


def update_file(fileName):
    initial = read_file(fileName)
    while True:
        current = read_file(fileName)
        if initial != current:
            with open('log.log' , 'w') as f:
                for line in current:
                    if line not in initial:
                        f.write(line)
                initial = current

@tasks.loop(seconds=1)
async def update_loop():
    update_file('latest.log')

@tasks.loop(seconds=1)
async def task():
    global ctx
    await ctx.edit(content = '"```" + read_file("log.log") + "```"')
    
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.startswith(commandPrefix + command):
        global ctx
        await message.channel.send(">>> "+ "Initializing Marinid Bot")
        ctx = await message.channel.send("```" + read_file('latest.log') + "```")
        update_loop.start()
        task.start(ctx)
        
bot.run(token)
