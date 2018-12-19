import discord
import json
import os
from datetime import datetime
from discord.ext import commands
from discord.ext.commands import Bot

print ('Lite-Bot is activating')


bot = Bot(command_prefix="!")
#prefix is !

bot.remove_command('help')
@bot.event
async def on_read():
	print("Client logged in")

#Message on user join
@bot.async_event
async def on_member_join(Member : discord.User):
	if (await check_config('join',Member.server) == 1):	
		with open('config.json', 'r') as j:
			config = json.load(j)
			await update_data(config, Member.server)
		channelId = config[Member.server.id]["joinleave"]
		await bot.send_message(bot.get_channel(channelId),"Welcome **"+Member.mention+"**")
	else:
		return
#Message on user leave
@bot.async_event
async def on_member_remove(Member : discord.User):
	if (await check_config('join',Member.server) == 1):	
		with open('config.json', 'r') as j:
			config = json.load(j)
			await update_data(config, Member.server)
		channelId = config[Member.server.id]["joinleave"]
		await bot.send_message(bot.get_channel(channelId),"**"+Member.name+"** has left the server")
	else:
		return

#Deletes messages that include key words, and discord invites
@bot.event
async def on_message(message, timeout=10):
	if (await check_config('swear',message.author.server) == 1):
		message.content = message.content.lower()
		for i in words:
			if str(i) in message.content:
				await bot.delete_message(message)
				await bot.send_message(message.channel, "No swearing")
				
	elif ((await check_config('invite',message.author.server) == 1)and(message.author.server_permissions.administrator == False)):
		if ("discord.gg" in message.content.lower()): 
			await bot.delete_message(message)
			await bot.send_message(message.channel, "Invites are not allowed in this server")
		
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
	elif ("".join(args) == "set"):
		await bot.say("Enables or disables a command, 1 = enable, 0 = disable.\n`!set kick 0`")
	else:
		embed=discord.Embed(title="Help")
		embed.add_field(name="!ban", value="!ban @user#0000", inline=False)
		embed.add_field(name="!kick", value="!kick @user#0000", inline=False)
		embed.add_field(name="!purge", value="!purge <NumberOfMessages>", inline=False)
		embed.add_field(name="!report", value="!report @user#0000 \"Report Content\"", inline=False)
		embed.add_field(name="!set", value="!set <Command> <1Or0>", inline=False)
		await bot.say(embed=embed)

#Kick user
@bot.command (pass_context=True)
async def kick(ctx, Member : discord.User):
	if (await check_config('kick',Member.server) == 1):
		if (Member.id == "227422944123551754" or Member.id == "405829095054770187"):
			await bot.say("Unable to kick that user")
		else:
			if (ctx.message.author.server_permissions.kick_members == True or ctx.message.author.server_permissions.administrator == True):
				try: 
					await bot.kick(Member)
					await bot.say("Successfully kicked **" + Member.name + "**")
				except discord.HTTPException:
					await bot.say("Unable to kick **" + Member.name + "**.")
			else:
				await bot.say("You do not have permission to kick** " + Member.name + "**")
	else:
		await bot.say("Kick is disabled")

#Ban user	
@bot.command (pass_context=True)
async def ban(ctx, Member : discord.User):
	if (await check_config('ban',Member.server) == 1):
		if (Member.id == "227422944123551754" or Member.id == "405829095054770187"):
			await bot.say("Unable to ban that user")
		else:
			if (ctx.message.author.server_permissions.ban_members == True or ctx.message.author.server_permissions.administrator == True):
				try: 
					await bot.ban(Member, delete_message_days=3)
					await bot.say("Successfully banned **" + Member.name + "**")
				except discord.HTTPException:
					await bot.say("Unable to ban **" + Member.name + "**")			
			else:
				await bot.say("You do not have permission to ban **" + Member.name + "**")
	else:
		await bot.say("Ban is disabled")
#Sends a dm to server's owner
@bot.command (pass_context=True)		
async def report(ctx, Member : discord.User, reportContent):
	if (await check_config('report',Member.server) == 1):
		await bot.send_message(ctx.message.author, "Your report against **" + Member.name+"#"+Member.discriminator + "** has been submitted to the server's owner")
		try:
			reportServer = ctx.message.author.server
			embed=discord.Embed(title="Submitted by "+ctx.message.author.name+"#"+ctx.message.author.discriminator, description=reportContent)
			embed.set_author(name="Report against "+Member.name+"#"+Member.discriminator)
			await bot.send_message(reportServer.owner, embed=embed)
		except discord.HTTPException:
			bot.send_message(ctx.message.author, "Your report against **" + Member.name + "** was unable to be sent to the server's owner")
		await bot.delete_message(ctx.message)
	else:
		await bot.say("Report is disabled")
		
#Purges messages	
@bot.command (pass_context=True)		
async def purge(ctx, numPurge : int,):
	if (await check_config('purge',ctx.message.author.server) == 1):
		await bot.delete_message(ctx.message)
		try:
			await bot.purge_from(ctx.message.channel,limit=numPurge)
		except discord.HTTPException:
			await bot.say("Unable to purge messages")
	else:
		await bot.say("Purge is disabled")

		
#Sets commands as enabled
@bot.command (pass_context=True)
async def enable(ctx, command : str):			
	with open('config.json', 'r') as j:
		config = json.load(j)
		await update_data(config, ctx.message.server)
	if (ctx.message.author.server_permissions.administrator == True):
		if (command == "ban"):
			config[ctx.message.server.id]["enabled"]["ban"] = 1
			await bot.say("Ban has been enabled")
		elif (command.lower() == 'kick'):
			config[ctx.message.server.id]["enabled"]['kick'] = 1
			await bot.say("Kick has been enabled")
		elif (command.lower() == 'purge'):
			config[ctx.message.server.id]["enabled"]['purge'] = 1
			await bot.say("Purge has been enabled")
		elif (command.lower() == 'join'):
			config[ctx.message.server.id]["enabled"]['join'] = 1
			await bot.say("Join messages has been enabled")
		elif (command.lower() == 'leave'):
			config[ctx.message.server.id]["enabled"]['leave'] = 1
			await bot.say("Leave messages has been enabled")
		elif (command.lower() == 'report'):
			config[ctx.message.server.id]["enabled"]['report'] = 1
			await bot.say("Reporting has been enabled")
		elif (command.lower() == 'invite'):
			config[ctx.message.server.id]["enabled"]['invite'] = 1
			await bot.say("Invite blocking has been enabled")
		elif (command.lower() == 'swear'):
			config[ctx.message.server.id]["enabled"]['swear'] = 1
			await bot.say("Swear blocking has been enabled")
		else:
			await bot.say("Invalid argument. Do `!help enable` for more info")
	else:
		bot.say("You must have administrator to enable or disable a command")
	with open("config.json", "w") as j:
		json.dump(config, j)
		
#Sets commands as disabled
@bot.command (pass_context=True)
async def disable(ctx, command : str):			
	with open('config.json', 'r') as j:
		config = json.load(j)
		await update_data(config, ctx.message.server)
	if (ctx.message.author.server_permissions.administrator == True):
		if (command == "ban"):
			config[ctx.message.server.id]["enabled"]["ban"] = 0
			await bot.say("Ban has been disabled")
		elif (command.lower() == 'kick'):
			config[ctx.message.server.id]["enabled"]['kick'] = 0
			await bot.say("Kick has been disabled")	
		elif (command.lower() == 'purge'):
			config[ctx.message.server.id]["enabled"]['purge'] = 0
			await bot.say("Purge has been disabled")
		elif (command.lower() == 'join'):
			config[ctx.message.server.id]["enabled"]['join'] = 0
			await bot.say("Join messages has been disabled")
		elif (command.lower() == 'leave'):
			config[ctx.message.server.id]["enabled"]['leave'] = 0
			await bot.say("Leave messages has been disabled")
		elif (command.lower() == 'report'):
			config[ctx.message.server.id]["enabled"]['report'] = 0
			await bot.say("Reporting has been disabled")
		elif (command.lower() == 'invite'):
			config[ctx.message.server.id]["enabled"]['invite'] = 0
			await bot.say("Invite blocking has been disabled")
		elif (command.lower() == 'swear'):
			config[ctx.message.server.id]["enabled"]['swear'] = 0
			await bot.say("Swear blocking has been disabled")
		else:
			await bot.say("Invalid argument. Do `!help disable` for more info")
	else:
		bot.say("You must have administrator to enable or disable a command")
	with open("config.json", "w") as j:
		json.dump(config, j)		
				
#Sets commands as either config or disabled
@bot.command (pass_context=True)
async def set(ctx, command : str, input : str):		
	print()
	with open('config.json', 'r') as j:
		config = json.load(j)
		await update_data(config, ctx.message.server)
	if (ctx.message.author.server_permissions.administrator == True):

		if (command.lower() == 'join' or command.lower() == 'leave'):
			channelId = input.replace('#', '').replace('<', '').replace('>', '')
			config[ctx.message.server.id]["joinleave"]= channelId
			await bot.say("Set join & leave messages channel to "+bot.get_channel(str(channelId)).mention)
		else:
			await bot.say("Invalid argument. Do `!help set` for more info")
	else:
		bot.say("You must have administrator to enable or disable a command")
	with open("config.json", "w") as j:
		json.dump(config, j)

#Function to update json file		
async def update_data(config, server):
	if not server.id in config:
		config[server.id] = {}
		config[server.id]["enabled"] = {}
		config[server.id]["enabled"]['ban'] = 1
		config[server.id]["enabled"]['kick'] = 1
		config[server.id]["enabled"]['purge'] = 1
		config[server.id]["enabled"]['join'] = 1
		config[server.id]["enabled"]['leave'] = 1
		config[server.id]["enabled"]['report'] = 0	
		config[server.id]["enabled"]['invite'] = 0
		config[server.id]["enabled"]['swear'] = 1
		config[server.id]["joinleave"] = ""

#Function to make it easier for commands to see if they are config
async def check_config(command, server):
	with open('config.json', 'r') as j:
		config = json.load(j)
	await update_data(config, server)
	return config[server.id]["enabled"][command]
	
print ('Ready\n')
print ('(ᵔᴥᵔ)\n')

#Opens words file
f = open('words.txt', 'r')
words = f.read().lower().splitlines()

#Opens discord key file
f = open('key.config', 'r')
key = f.read()

#Bot Token
bot.run(key)
