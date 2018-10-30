import discord
import random
from datetime import datetime
from random import randint
from discord.ext import commands
from discord.ext.commands import Bot

print ('Lite-Bot is activating')

bot = Bot(command_prefix="!")
#prefix is !

bot.remove_command('help')
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

#Deletes messages that include key words
@bot.event
async def on_message(message, timeout=10):
	message.content = message.content.lower()
	for i in words:
		if str(i) in message.content:
			await bot.delete_message(message)
			await bot.send_message(message.channel, "No swearing")
			#print ("Deleted Message By: " + str(message.author))
			
	await bot.process_commands(message)

#Replies to invalid commands	
@bot.event
async def on_command_error(error, ctx):
	if isinstance(error, commands.CommandNotFound):
		await bot.send_message(ctx.message.channel,"Command not found, check out !help")
	if isinstance(error, commands.MissingRequiredArgument):
		await bot.send_message(ctx.message.channel,"Missing required arguments, check out !help")
	if isinstance(error, commands.BadArgument):
		await bot.send_message(ctx.message.channel,"Invalid argument, check out !help")
	if isinstance(error, commands.TooManyArguments):
		await bot.send_message(ctx.message.channel,"Too many arguments, check out !help")		

#General help & extra detail	
@bot.command (pass_context=True)
async def help(ctx, *args):
	if ("".join(args) == "ban"):
		await bot.say("Bans an user and deletes their messages from the past 3 days\n`!ban @user#0000`")
	elif ("".join(args) == "kick"):
		await bot.say("Kicks an user\n`!kick @user#0000`")
	elif ("".join(args) == "purge"):
		await bot.say("Mass deletes messages\n`!purge 30`")
	elif ("".join(args) == "report"):
		await bot.say("Sends a report to the server's owner, requires double quotes around the report content\n`!report @user#0000 \"Stealing the Village gold\"`")
	else:
		embed=discord.Embed(title="Help")
		embed.add_field(name="!ban", value="!ban @user#0000", inline=False)
		embed.add_field(name="!kick", value="!kick @user#0000", inline=False)
		embed.add_field(name="!purge", value="!purge <NumberOfMessages>", inline=False)
		embed.add_field(name="!report", value="!report @user#0000 \"Report Content\"", inline=False)
		await bot.say(embed=embed)

#Kick users
@bot.command (pass_context=True)
async def kick(ctx, Member : discord.User):
	if (Member.id == "342342" or Member.id == "342342"):
		bot.say("Unable to kick that user")
	else:
		if (ctx.message.author.server_permissions.kick_members == True or ctx.message.author.server_permissions.administrator == True):
			try: 
				await bot.kick(Member)
				await bot.say("Successfully kicked **" + Member.name + "**")
			except discord.HTTPException:
				await bot.say("Unable to kick **" + Member.name + "**.")
		else:
			await bot.say("You do not have permission to kick** " + Member.name + "**")

#Ban users		
@bot.command (pass_context=True)
async def ban(ctx, Member : discord.User):
	if (Member.id == "342342" or Member.id == "342342"):
		bot.say("Unable to ban that user")
	else:
		if (ctx.message.author.server_permissions.ban_members == True or ctx.message.author.server_permissions.administrator == True):
			try: 
				await bot.ban(Member, delete_message_days=3)
				await bot.say("Successfully banned **" + Member.name + "**")
			except discord.HTTPException:
				await bot.say("Unable to ban **" + Member.name + "**")			
		else:
			await bot.say("You do not have permission to ban **" + Member.name + "**")

#Sends a dm to server's owner
@bot.command (pass_context=True)		
async def report(ctx, Member : discord.User, reportContent):
	await bot.send_message(ctx.message.author, "Your report against **" + Member.name+"#"+Member.discriminator + "** has been submitted to the server's owner")
	try:
		reportServer = ctx.message.author.server
		embed=discord.Embed(title="Submitted by "+ctx.message.author.name+"#"+ctx.message.author.discriminator, description=reportContent)
		embed.set_author(name="Report against "+Member.name+"#"+Member.discriminator)
		await bot.send_message(reportServer.owner, embed=embed)
	except discord.HTTPException:
		bot.send_message(ctx.message.author, "Your report against **" + Member.name + "** was unable to be sent to the server's owner")
	await bot.delete_message(ctx.message)

#Purges messages	
@bot.command (pass_context=True)		
async def purge(ctx, numPurge : int):
	await bot.delete_message(ctx.message)	
	try:
		await bot.purge_from(ctx.message.channel,limit=numPurge)
	except discord.HTTPException:
		await bot.say("Unable to purge messages")

print ('Ready\n')
print ('(ᵔᴥᵔ)\n')

#Opens words file
f = open('words.txt', 'r')
words = f.read().splitlines()

#Opens discord key file
f = open('key.config', 'r')
key = f.read()

#Bot Token
bot.run(key)
