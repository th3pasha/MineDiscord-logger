import requests
import json
import discord
from discord.ext import tasks

intents = discord.Intents.default()
intents.message_content = True

fileName= 'latest.log'
infoFileName = 'info.log'
serverIP = '34.175.106.153'

roleID = '1075921667454419036'

commandPrefix = '/'
command = 'minecraft'
token = ''

bot = discord.Client(intents=intents)

def readinfo_file():
    with open(infoFileName) as f:
        return f.read()

def dump_info():
    info = get_info()
    with open(infoFileName, 'w') as f:
        f.write(info)
        f.close

def get_server(serverIP):
    response = requests.get('https://mcapi.us/server/status?ip=' + serverIP)
    if response.status_code == 200:
        data = response.json()
    else :
        return 'request failed'
    return data

def get_info():
    data = get_server(serverIP)
    serverStatus = ''
    serverBoolStatus = data['online']
    if serverBoolStatus == True:
        serverStatus = 'The server is online'
    else:
        serverStatus = 'The server is not online'
    motd = data['motd']
    nowPlayers = str(data['players']['now'])
    maxPlayers = str(data['players']['max'])
    serverVersion = data['server']['name']

    return serverStatus + '\n\nServer Name: Marinid Dynasty\nIP Address: ['+serverIP+']\nVersion: '+serverVersion+'\nGame Mode: Hard, pussy.\nPlayers Online: '+nowPlayers+'/'+maxPlayers+'\n\nDescription: \n\n' + motd    


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
    if message.content.startswith(commandPrefix + "mcinfo"):
        global ctx_info
        await message.channel.send(">>> "+ "<@&"+roleID +">")
        await message.channel.send(">>> Initializing Marinid Bot ")
        ctx_info = await message.channel.send("```" + readinfo_file() + "```")
        while True:
            dump_info()
            await ctx_info.edit(content = "```" + readinfo_file() + "```")
    if message.content.startswith(commandPrefix + command):
        global ctx
        await message.channel.send(">>> "+ "<@&"+roleID +">")
        await message.channel.send(">>> "+ "Initializing Marinid Bot")
        ctx = await message.channel.send("```" + read_file(fileName) + "```")
        while True:
            await ctx.edit(content = "```" + read_file(fileName) + "```")

bot.run(token)
