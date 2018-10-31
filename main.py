import discord
from discord.ext import commands
from discord.ext.commands import Bot
from collections import deque
import config

prefix = config.Prefix
client = Bot(description=config.Description, command_prefix=prefix)
server = None
tagchannel = None
serverroles = None
allowedRoles = config.AllowedRoles

@client.event
async def on_ready():
    print('Logged in as {}'.format(client.user.name))
    return await client.change_presence(game=discord.Game(name='Giving Roles to users'))

@client.event
async def on_message(message):
    print(message.author.name + ': ' + message.content)
    serverroles = message.server.roles
    if message.author == client.user:
        return
    elif message.content[0] != prefix:
        return
    elif message.channel.id != config.TagChannel:
        print(message.author.name + ' just tried to use a command outside of Tag Channel!')
    elif str.upper(message.content) == prefix + 'ROLES':
        for role in allowedRoles:
                await client.send_message(message.channel, role)
    elif str.upper(message.content) == prefix + 'MY ROLES':
        for role in message.author.roles:
            if str(role) != '@everyone':
                await client.send_message(message.channel, role)
    else:
        RoleFound = False
        for r in allowedRoles:
            if str.upper(message.content) == prefix + str.upper(r):
                RoleFound = True
                GivingRole = discord.utils.get(message.server.roles, name = str(r))
                if HasRole(GivingRole, message):
                    await client.send_message(message.channel, "Removing your " + r + " Role!")
                    await client.remove_roles(message.author, GivingRole)
                else:
                    await client.send_message(message.channel, "Giving you " + r + " Role!")
                    await client.add_roles(message.author, GivingRole)
                    
        
        if RoleFound == False:
            await client.send_message(message.channel, "That role is either not created or is not allowed to be added to users!")

def AllRoles(message):
    for r in allowedRoles:
        client.send_message(tagchannel, r)
        
def HasRole(Role, message):
    for r in message.author.roles:
        if Role == r:
            return True

client.run(config.Token)
