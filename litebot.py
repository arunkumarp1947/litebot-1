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
	try:
		if (await check_config('join',Member.server, False) == 1):	
			channelId = await check_config('joinleaveChannel',Member.server, True)
			await bot.send_message(bot.get_channel(channelId),"Welcome **"+Member.mention+"**")
		else:
			return
	except:
		await bot.say("Error")
		print("Error")

#Message on user leave
@bot.async_event
async def on_member_remove(Member : discord.User):
	try:
		if (await check_config('join',Member.server, False) == 1):	
			channelId = await check_config('joinleaveChannel',Member.server, True)
			await bot.send_message(bot.get_channel(channelId),"**"+Member.name+"** has left the server")
		else:
			return
	except:
		await bot.say("Error")
		print("Error")

#Deletes messages that include key words, and discord invites
@bot.event
async def on_message(message, timeout=10):
	unableToCheckMessages = False
	if (message.channel.is_private==False and (message.author != message.server.me)):
		if (await check_config('swear', message.author.server, False) >= 1):
			if (message.server.me.server_permissions.manage_messages == True or message.server.me.server_permissions.administrator == True):
				message.content = message.content.lower()
				toDelete = False
				for i in words1:
					if ((str(i) in message.content) and (await check_config('swear', message.author.server, False) >= 1)):
						toDelete = True
						
				for i in words2:
					if ((str(i) in message.content) and (await check_config('swear', message.author.server, False) >= 2)):
						toDelete = True
						
				for i in words3:
					if ((str(i) in message.content) and (await check_config('swear', message.author.server, False) >= 3)):	
						toDelete = True
				
				if (toDelete == True):
					await bot.delete_message(message)
					await bot.send_message(message.channel, "No swearing")
			else:
				unableToCheckMessages = True			
		elif ((await check_config('invite',message.author.server, False) == 1)and(message.author.server_permissions.administrator == False)):
			if (message.server.me.server_permissions.manage_messages == True or message.server.me.server_permissions.administrator == True):
				if ("discord.gg" in message.content.lower()): 
					await bot.delete_message(message)
					await bot.send_message(message.channel, "Invites are not allowed in this server")
			else:
				unableToCheckMessages = True
		if (unableToCheckMessages):
			await bot.send_message(message.channel,"Unable to check messages as I do not have permission to delete messages.\nDisabling Swear Blocking and Invite Blocking now")
			await bot_disable(message.server, 'swear')
			await bot_disable(message.server, 'invite')
			unableToCheckMessages = False
		await bot.process_commands(message)
	else: 
		return

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
	try:
		if ("".join(args) == "ban"):
			await bot.say("Bans an user and deletes their messages from the past 3 days\n`!ban @user#0000`")
		elif ("".join(args) == "kick"):
			await bot.say("Kicks an user\n`!kick @user#0000`")
		elif ("".join(args) == "purge"):
			await bot.say("Mass deletes messages\n`!purge 30`")
		elif ("".join(args) == "report"):
			await bot.say("Sends a report to the server's owner, requires double quotes around the report content\n`!report @user#0000 \"Stealing the Village gold\"`")
		elif ("".join(args) == "set"):
			await bot.say("Sets a command to a value\n `!set join #general`")
		elif ("".join(args) == "enable"or"".join(args) == "disable"):
			await bot.say("Enables or disables a command\n `!enable kick`")
		else:
			embed=discord.Embed(title="Help")
			embed.add_field(name="!ban", value="!ban @user#0000", inline=False)
			embed.add_field(name="!kick", value="!kick @user#0000", inline=False)
			embed.add_field(name="!purge", value="!purge <NumberOfMessages>", inline=False)
			embed.add_field(name="!report", value="!report @user#0000 \"Report Content\"", inline=False)
			embed.add_field(name="!enable", value="!enable <kick>", inline=False)
			embed.add_field(name="!disable", value="!disable <command>", inline=False)
			embed.add_field(name="!set", value="!set <command> <channel>", inline=False)
			await bot.say(embed=embed)
	except:
		await bot.say("Error")
		print("Error")
#Kick user
@bot.command (pass_context=True)
async def kick(ctx, Member : discord.User):
	try:
		if (await check_config('kick',Member.server, False) == 1):
			if (Member.id == "227422944123551754" or Member.id == "405829095054770187"):
				await bot.say("Unable to kick that user")
			else:
				if (ctx.message.server.me.server_permissions.kick_members == True or ctx.message.server.me.server_permissions.administrator == True):
					if (ctx.message.author.server_permissions.kick_members == True or ctx.message.author.server_permissions.administrator == True):
						try:
							await bot.kick(Member)
							await bot.say("Successfully kicked **" + Member.name + "**")
						except discord.HTTPException:
							await bot.say("Unable to kick **" + Member.name + "**.")
					else:
						await bot.say("You do not have permission to kick** " + Member.name + "**")
				else:
					await bot.say("Sorry, I do not have permission to ban\nDisabling kick now")
					await bot_disable(ctx.message.server, "kick")
		else:
			await bot.say("Kick is disabled")
	except:
		await bot.say("Error")
		print("Error")
#Ban user	
@bot.command (pass_context=True)
async def ban(ctx, Member : discord.User):
	try:
		if (await check_config('ban',Member.server, False) == 1):
			if (Member.id == "227422944123551754" or Member.id == "405829095054770187"):
				await bot.say("Unable to ban that user")
			else:
				if (ctx.message.server.me.server_permissions.ban_members or ctx.message.server.me.server_permissions.ban_members):
					if (ctx.message.author.server_permissions.ban_members == True or ctx.message.author.server_permissions.administrator == True):
						try: 
							await bot.ban(Member, delete_message_days=3)
							await bot.say("Successfully banned **" + Member.name + "**")
						except discord.HTTPException:
							await bot.say("Unable to ban **" + Member.name + "**")			
					else:
						await bot.say("You do not have permission to ban **" + Member.name + "**")
				else:
					await bot.say("Sorry, I do not have permission to ban.\nDisabling !ban now")
					await bot_disable(ctx.message.server, "ban")
		else:
			await bot.say("Ban is disabled")
	except:
		await bot.say("Error")
		print("Error")
#Sends a report to the report channel
@bot.command (pass_context=True)		
async def report(ctx, Member : discord.User, reportContent):
	try:
		if (await check_config('report',Member.server, False) == 1):
			await bot.send_message(ctx.message.author, "Your report against **"+Member.name+"#"+Member.discriminator+"** has been submitted to the server's owner")
			try:
				channelId = await check_config('reportChannel',Member.server, True)
				
				if "#" in channelId:
					channelId = channelId.replace('#', '')
					reportSendLocation = bot.get_channel(channelId)
				elif "@" in channelId: 
					channelId = channelId.replace('@', '')
					reportSendLocation = await bot.get_user_info(channelId)
				
				embed=discord.Embed(title="Submitted by "+ctx.message.author.name+"#"+ctx.message.author.discriminator, description=reportContent)
				embed.set_author(name="Report against "+Member.name+"#"+Member.discriminator)
				await bot.send_message(reportSendLocation, embed=embed)
			except discord.HTTPException:
				bot.send_message(ctx.message.author, "Your report against **" + Member.name + "** was unable to be sent")
			await bot.delete_message(ctx.message)
		else:
			await bot.say("Report is disabled")
	except:
		await bot.say("Error")
		print("Error")
#Purges messages	
@bot.command (pass_context=True)#Need to add perm checker
async def purge(ctx, numPurge : int,):
	try:
		if (await check_config('purge',ctx.message.author.server, False) == 1):
			if (ctx.message.server.me.server_permissions.manage_messages == True or ctx.message.server.me.server_permissions.administrator == True):
				if (ctx.message.author.server_permissions.manage_messages == True or ctx.message.author.server_permissions.administrator == True):
					await bot.delete_message(ctx.message)
					try:
						await bot.purge_from(ctx.message.channel,limit=numPurge)
					except discord.HTTPException:
						await bot.say("Unable to purge messages")
			else:
				await bot.say("Sorry, I do not have permission to delete messages. \nDisabling purge now")
				await bot_disable(ctx.message.server, "purge")
		else:
			await bot.say("Purge is disabled")		
	except:
		await bot.say("Error")
		print("Error")
		
#Sets commands as enabled
@bot.command (pass_context=True)
async def enable(ctx, command : str):
	try:			
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
	except:
		await bot.say("Error")
		print("Error")
		
#Sets commands as disabled
@bot.command (pass_context=True)
async def disable(ctx, command : str):		
	try:	
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
			bot.say("You must have administrator to set a command")
		with open("config.json", "w") as j:
			json.dump(config, j)
	except:
		await bot.say("Error")
		print("Error")
				
#Sets commands 
@bot.command (pass_context=True)
async def set(ctx, command : str, input : str):	
	try:	
		with open('config.json', 'r') as j:
			config = json.load(j)
			await update_data(config, ctx.message.server)

		if (ctx.message.author.server_permissions.administrator == True):

			if (command.lower() == 'join' or command.lower() == 'leave' or command.lower() == 'joinleave'):
				channelId = input.replace('#', '').replace('<', '').replace('>', '')

				if (bot.get_channel(channelId)==None):
					await bot.say("Not a valid channel")
				else:
					await bot.say("Set join & leave messages channel to "+input)
					config[ctx.message.server.id]["joinleaveChannel"]= channelId
				
			elif (command.lower() == 'report'):
				channelId = input.replace('<', '').replace('>', '').replace('!', '')
				await bot.say("Set report messages channel to "+input)
				config[ctx.message.server.id]["reportChannel"]= channelId
				
			elif (command.lower() == 'swear'):
				config[ctx.message.server.id]["enabled"]["swear"]= int(input)
				await bot.say("Set swear blocking level to "+input)
			
			else:
				await bot.say("Invalid argument. Do `!help set` for more info")
		else:
			bot.say("You must have administrator to enable or disable a command")
		with open("config.json", "w") as j:
			json.dump(config, j)
	except:
		await bot.say("Error")
		print("Error")

#Function to disable bot commands serverside
async def bot_disable(server, command):
	with open('config.json', 'r') as j:
		config = json.load(j)
		await update_data(config, server)		
	config[server.id]["enabled"][command] = 0
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
		config[server.id]["joinleaveChannel"] = ""
		config[server.id]["reportChannel"] = ""

#Function to make it easier for commands to check their config
async def check_config(command, server, outsideEnabled):
	with open('config.json', 'r') as j:
		config = json.load(j)
	await update_data(config, server)
	if (outsideEnabled == False):
		return config[server.id]["enabled"][command]
	else:
		return config[server.id][command]
		
print ('Ready\n')
print ('(ᵔᴥᵔ)\n')

#Opens words file
f = open('words/words1.txt', 'r')
words1 = f.read().lower().splitlines()
f = open('words/words2.txt', 'r')
words2 = f.read().lower().splitlines()
f = open('words/words3.txt', 'r')
words3 = f.read().lower().splitlines()

#Opens discord key file
f = open('key.config', 'r')
key = f.read()

#Bot Token
bot.run(key)