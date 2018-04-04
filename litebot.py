import discord
import random
from random import randint
from discord.ext.commands import Bot

bot = Bot(command_prefix="/")
#prefix is !

@bot.event
async def on_read():
    print("Client logged in")

#Welcome @user
@bot.async_event
async def on_member_join(Member : discord.User):
    await bot.send_message(bot.get_channel(Member.server.id),"Welcome **"+Member.mention+"**")

#user has left the server
@bot.async_event
async def on_member_remove(Member : discord.User):
    await bot.send_message(bot.get_channel(Member.server.id),"**"+Member.name+"** has left the server")

#Deletes messages that include words
@bot.event
async def on_message(message, timeout=10):
	message.content = message.content.lower()
	for i in words:
		if str(i) in message.content:
			await bot.delete_message(message)
			await bot.send_message(message.channel, 'No swearing')
			print ("Deleted Message By: " + str(message.author))

print ('Lite-Bot is activating')
print ('Ready')
print ('')
print ('(ᵔᴥᵔ)')
print ('')

#Opens words file
f = open('words.txt', 'r')
words = f.read().splitlines()

#Opens discord key file
f = open('key.config', 'r')
key = f.read()

#Bot Token
bot.run(key)