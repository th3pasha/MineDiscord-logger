import discord
from discord.ext import tasks

intents = discord.Intents.default()
intents.message_content = True

fileName= 'latest.log'

commandPrefix = '/'
command = 'minecraft'
token = 'MTA3ODA3NjMzMTg1NTcyODgwMA.G-qlre.xVYtjK9AGHTqjzvz1OvroRLccw3nDbqck9K3CU'

bot = discord.Client(intents=intents)

def filter_line(string):
    filtered = ''
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
            filtered += line.replace("[Server thread/INFO]", "") + '\n'

    return filtered        

def read_file(fileName):
    fileContent = ''
    with open(fileName, 'r') as f:
        file_lines = f.readlines()[-10:]
        for line in file_lines:
            fileContent += line
    return filter_line(fileContent)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.startswith(commandPrefix + command):
        global ctx
        await message.channel.send(">>> "+ "Initializing Marinid Bot")
        ctx = await message.channel.send("```" + read_file(fileName) + "```")
        while True:
            await ctx.edit(content = "```" + read_file(fileName) + "```")

bot.run(token)
