import discord

intents = discord.Intents.default()
intents.message_content = True

command_prefix = '/'
command = 'minecraft'
token = 'MTA3ODA3NjMzMTg1NTcyODgwMA.G-qlre.xVYtjK9AGHTqjzvz1OvroRLccw3nDbqck9K3CU'

client = discord.Client(intents=intents)
client_message = ""

def read_file(fileName):
    with open(fileName, 'r') as f:
        file_content = f.read()
    return file_content

def filter_file(fileName, newFileName):
    with open(fileName, 'r') as f:
        for line in f:
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
            else:
                with open(newFileName, 'a') as out_file:
                    out_file.write(line)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(command_prefix + command):
        await message.channel.send(">>> "+ "Initializing Marinid Bot")
        client_message = await message.channel.send("```"+read_file("log.log")+"```")

    if message.content.startswith(command_prefix + "update"):
        bot_channel = client.get_channel(message.channel.id)
        bot_update = await bot_channel.fetch_message(client_message.id)
        await bot_update.edit(content = read_file("log.log"))

client.run(token)
