import discord

intents = discord.Intents.default()
intents.message_content = True

token = 'MTA3ODA3NjMzMTg1NTcyODgwMA.G-qlre.xVYtjK9AGHTqjzvz1OvroRLccw3nDbqck9K3CU'
command_prefix = '/'
command = 'minecraft'

client = discord.Client(intents=intents)

def read_file(filename):
    with open(filename, 'r') as f:
        file_size = f.readlines()
        file_content = f.read()
    return file_content

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(command_prefix+command):
        await message.channel.send(message)

client.run('MTA3ODA3NjMzMTg1NTcyODgwMA.G-qlre.xVYtjK9AGHTqjzvz1OvroRLccw3nDbqck9K3CU')
