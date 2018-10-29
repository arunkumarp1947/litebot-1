import discord
import random
from random import randint
from discord.ext.commands import Bot

bot = Bot(command_prefix="!")
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
			
	await bot.process_commands(message)

@bot.command (pass_context=True)
async def kick(ctx, Member : discord.User):
	if (ctx.message.author.server_permissions.kick_members == True or ctx.message.author.server_permissions.administrator == True):
		try: 
			await bot.kick(Member)
			await bot.say("Successfully kicked **" + Member.name + "**")
		except discord.HTTPException:
			await bot.say("Unable to kick **" + Member.name + "**.")
	else:
		await bot.say("You do not have permission to kick** " + Member.name + "**")			
@bot.command (pass_context=True)
async def ban(ctx, Member : discord.User):
	if (ctx.message.author.server_permissions.ban_members == True or ctx.message.author.server_permissions.administrator == True):
		try: 
			await bot.ban(Member, delete_message_days=3)
			await bot.say("Successfully banned **" + Member.name + "**")
		except discord.HTTPException:
			await bot.say("Unable to ban **" + Member.name + "**")			
	else:
		await bot.say("You do not have permission to ban **" + Member.name + "**")
	
#settings.owner
	
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
