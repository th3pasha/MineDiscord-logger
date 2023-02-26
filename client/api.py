import discord
import requests
import json
from discord.ext import tasks

intents = discord.Intents.default()
intents.message_content = True

fileName= 'info.log'

serverIP = '34.175.106.153'
roleID = '1075921667454419036'

commandPrefix = '/'
command = 'mcinfo'
token = 'MTA3ODA3NjMzMTg1NTcyODgwMA.G-qlre.xVYtjK9AGHTqjzvz1OvroRLccw3nDbqck9K3CU'

bot = discord.Client(intents=intents)

def read_file():
    with open(fileName) as f:
        return f.read()

def dump_info():
    info = get_info()
    with open(fileName, 'w') as f:
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

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.startswith(commandPrefix + command):
        global ctx
        await message.channel.send(">>> "+ "<@&"+roleID +">")
        await message.channel.send(">>> Initializing Marinid Bot ")
        ctx = await message.channel.send("```" + read_file() + "```")
        while True:
            dump_info()
            await ctx.edit(content = "```" + read_file() + "```")


bot.run(token)
