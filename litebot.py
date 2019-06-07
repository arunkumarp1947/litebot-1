import discord
import json
import os
import sys
from datetime import datetime
from discord.ext import commands
from discord.ext.commands import Bot

print('Lite-Bot is activating')

bot = Bot(command_prefix="+")
# prefix is +

bot.remove_command('help')
@bot.event
async def on_ready():
	print('Ready\n')
	print("                     ")
	print("	  .__(.)< (MEOW)    ")
	print("	  \___)             ")
	print("~~~~~~~~~~~~~~~~~~~~~")
	await bot.change_presence(game=discord.Game(name='over the Server | +help',type=3,url="http://jxhub.xyz"))
	updateConsole()

@bot.async_event
async def on_server_join(Server: discord.Server):
	updateConsole()

@bot.async_event
async def on_server_remove(Server: discord.Server):
	updateConsole()

def updateConsole():
	print("{members} users in {servers} servers".format(members=str(
		len(set(bot.get_all_members()))-1), servers=str(len(bot.servers))), end='\r')
	with open('servers.txt', 'w') as f:
		for item in bot.servers:
			f.write("%s\n" % item)

# Message on user join
@bot.async_event
async def on_member_join(Member: discord.User):
	try:
		# Join message
		if (await check_config('join', Member.server, False)):
			channel = bot.get_channel(await check_config('joinleaveChannel', Member.server, True))
			joinMsgText = await check_config('joinMsgText', Member.server, True)
			if joinMsgText == "":
				joinMsgText = "Welcome {user}"
			if (channel != None):
				await bot.send_message(channel, joinMsgText.format(user=Member.mention, server=Member.server.name))

		# Join dm
		if (await check_config('joinDm', Member.server, False)):
			dmText = (await check_config('joinDmText', Member.server, True))
			if (dmText == ""):
				return
			elif (len(dmText) >= 200):
				return
			await bot.send_message(Member, dmText.format(user=Member.mention, server=Member.server.name))
		updateConsole()
	except:
		print("Error")

# Message on user leave
@bot.async_event
async def on_member_remove(Member: discord.User):
	try:
		if (await check_config('leave', Member.server, False)):
			channel = bot.get_channel(await check_config('joinleaveChannel', Member.server, True))
			leaveMsgText = await check_config('leaveMsgText', Member.server, True)
			if leaveMsgText == "":
				leaveMsgText = "{user} has left the server"
			if (channel != None):
				await bot.send_message(channel, leaveMsgText.format(user=Member.name, server=Member.server.name))
		updateConsole()
	except:
		print("Error")

# Deletes messages that include key words, and discord invites
@bot.event
async def on_message(message, timeout=10):
	unableToCheckMessages = False
	# Ensures bot only responds to valid message
	if (message.channel.is_private == False and message.author != message.server.me):
		# Makes sure swear is enabled
		if (await check_config('swear', message.author.server, False)):
			# Checks if bot has proper permissions
			if (message.server.me.server_permissions.manage_messages or message.server.me.server_permissions.administrator):
				toDelete = False
				# Checks each word for swears
				for i in words1:
					if ((str(i) in message.content.lower()) and (await check_config('swear', message.author.server, True) >= 1)):
						toDelete = True

				for i in words2:
					if ((str(i) in message.content.lower()) and (await check_config('swear', message.author.server, True) >= 2)):
						toDelete = True

				for i in words3:
					if ((str(i) in message.content.lower()) and (await check_config('swear', message.author.server, True) >= 3)):
						toDelete = True

				# Deletes message if contains swear
				if toDelete:
					await bot.delete_message(message)
					await bot.send_message(message.channel, "No swearing "+message.author.mention)
					return
			else:
				unableToCheckMessages = True
		# Checks for server invites
		if ((await check_config('invite', message.author.server, False))and(message.author.server_permissions.administrator == False)):
			if (message.server.me.server_permissions.manage_messages or message.server.me.server_permissions.administrator):
				if ("discord.gg" in message.content.lower()):
					await bot.delete_message(message)
					await bot.send_message(message.channel, "Invites are not allowed in this server")
					return
			else:
				unableToCheckMessages = True
		# Checks for links
		if ((await check_config('link', message.author.server, False))and(message.author.server_permissions.administrator == False)):
			if (message.server.me.server_permissions.manage_messages or message.server.me.server_permissions.administrator):
				if ("http://" in message.content.lower()or("https://" in message.content.lower())):
					await bot.delete_message(message)
					await bot.send_message(message.channel, "Links are not allowed in this server")
					return
			else:
				unableToCheckMessages = True
		# Disables commands if bot doesn't have permission to delete messages
		if (unableToCheckMessages):
			try:
				await bot_disable(message.server, 'swear')
				await bot_disable(message.server, 'invite')
				await bot_disable(message.server, 'link')
				await bot.send_message(message.channel, "Unable to check messages as I do not have permission to delete messages.\nDisabling Swear Blocking, link blocking, and Invite Blocking now")
				unableToCheckMessages = False
			except:
				return
		try:
			await bot.process_commands(message)
		except:
			await bot.say("Error")
			print("Error")

		if ("<@405829095054770187>" in message.content)and("+purge" not in message.content):
			await bot.send_message(message.channel, "Hi, I'm lite-bot, a administrative bot designed to make running a server easier. My prefix is `+` and you can see my commands using `+help`")
			return
		# Easter egg to respond to rude users
		runOnce = False
		async for message in bot.logs_from(message.channel, limit=2):
			if runOnce == False:
				if ("stfu" in message.content.lower())or("die" in message.content.lower())or("kys" in message.content.lower()):
					sayNo = True
				else:
					sayNo = False
				runOnce = True
			else:
				if (message.author == bot.user)and(sayNo):
					await bot.send_message(message.channel, "No")
	else:
		return

# Replies to invalid commands
@bot.event
async def on_command_error(error, ctx):
	if isinstance(error, commands.CommandNotFound):
		await bot.send_message(ctx.message.channel, "Command not found, check out +help")
	if isinstance(error, commands.MissingRequiredArgument):
		await bot.send_message(ctx.message.channel, "Missing required arguments, check out +help")
	if isinstance(error, commands.BadArgument):
		await bot.send_message(ctx.message.channel, "Invalid argument, check out +help")
	if isinstance(error, commands.TooManyArguments):
		await bot.send_message(ctx.message.channel, "Too many arguments, check out +help")

# General help & extra detail
@bot.command(pass_context=True)
async def help(ctx, *args):
	#Ping
	input=("".join(args)).lower()
	if (input == "ping"):
		embed=discord.Embed(title="Ping",color=0xff8000)
		embed.add_field(name="Description", value="Displays the latency between discord and litebot", inline=False)
		embed.add_field(name="Usage", value="`+ping`", inline=False)
		await bot.say(embed=embed)
	#Role
	elif (input == "role"):
		embed=discord.Embed(title="Role",color=0xff8000)
		embed.add_field(name="Description", value="Allows users to add or remove themselves from roles easily.", inline=False)
		embed.add_field(name="Usage", value="`+role <role name>`", inline=False)
		await bot.say(embed=embed)
	#Report
	elif (input == "report"):
		embed=discord.Embed(title="Report",color=0xff8000)
		embed.add_field(name="Description", value="Use report to report misbehaving users to the server admin. Messages are deleted after you send them so there's no need to worry about them finding out", inline=False)
		embed.add_field(name="Usage", value="`+report @username#0000 Stealing the village gold`", inline=False)
		await bot.say(embed=embed)
	#Kick
	elif (input == "kick"):
		embed=discord.Embed(title="Kick",color=0xff8000)
		embed.add_field(name="Description", value="Kicks a user from the server.", inline=False)
		embed.add_field(name="Usage", value="`+kick @username#0000`", inline=False)
		await bot.say(embed=embed)
	#Ban
	elif (input == "ban"):
		embed=discord.Embed(title="Kick",color=0xff8000)
		embed.add_field(name="Description", value="Bans a user from the server. You can optionally specify an amount of days of which that user's messages will be deleted.", inline=False)
		embed.add_field(name="Usage", value="`+ban @username#0000 <Days of messages to delete`", inline=False)
		await bot.say(embed=embed)
	#Purge
	elif (input == "purge"):
		embed=discord.Embed(title="Purge",color=0xff8000)
		embed.add_field(name="Description", value="Mass deletes up to 100 messages in the current channel. Can optionally specify a single user to delete messages by.", inline=False)
		embed.add_field(name="Usage", value="`+purge 40 @username#0000`", inline=False)
		await bot.say(embed=embed)
	#Config
	elif (input == "config"):
		embed=discord.Embed(title="Config",color=0xff8000)
		embed.add_field(name="Description", value="Edits the config for the server. Can configure `joinmsg`, `leavemsg`, `swear`, `joindm` or `roles`.\nTo configure what roles a user can add themselves to using `+role` do `+config roles <role1>;<role2>;<role3>` with `;` seperating the role names", inline=False)
		embed.add_field(name="Usage", value="`+config <command> <value>`", inline=False)
		await bot.say(embed=embed)
	#Enable
	elif (input == "enable"):
		embed=discord.Embed(title="Enable",color=0xff8000)
		embed.add_field(name="Description", value="Enables a command. Can enable `+kick`, `+role`, `+report`, `join messages`, `leave messages`, `swear blocking`, `invite blocking`, `link blocking`, and `Join DM`.", inline=False)
		embed.add_field(name="Usage", value="`+enable <command>`", inline=False)
		await bot.say(embed=embed)
	#Disable
	elif (input == "disable"):
		embed=discord.Embed(title="Disable",color=0xff8000)
		embed.add_field(name="Description", value="Disables a command. Can disable `+kick`, `+role`, `+report`, `join messages`, `leave messages`, `swear blocking`, `invite blocking`, `link blocking`, and `Join DM`", inline=False)
		embed.add_field(name="Usage", value="`+disable <command>`", inline=False)
		await bot.say(embed=embed)
	#Check
	elif (input == "check"):
		embed=discord.Embed(title="Check",color=0xff8000)
		embed.add_field(name="Description", value="Displays the servers config", inline=False)
		embed.add_field(name="Usage", value="`+check`", inline=False)
		await bot.say(embed=embed)
	#Join Message
	elif (input == "join" or input == "join message" or input == "joinmsg"):
		embed=discord.Embed(title="Join Message",color=0xff8000)
		embed.add_field(name="Description", value="Sends a message when a user joins the server. Set the message using `+config joinmsg <Join Message Text>` Use `{user}` and `{server}` to put the users or servers name in.", inline=False)
		await bot.say(embed=embed)
	#Leave Message
	elif (input == "leave" or input == "leave message" or input == "leavemsg"):
		embed=discord.Embed(title="Leave Message",color=0xff8000)
		embed.add_field(name="Description", value="Sends a message when a user leaves the server. Set the message using `+config leavemsg <Leave Message Text>` Use `{user}` and `{server}` to put the users or servers name in.", inline=False)
		await bot.say(embed=embed)
	#Swear blocking
	elif (input == "swear" or input == "swear blocking"):
		embed=discord.Embed(title="Swear Blocking",color=0xff8000)
		embed.add_field(name="Description", value="Deletes messages containing swear words. Set the swear blocking level using `+config swear <value>`.", inline=False)
		await bot.say(embed=embed)
	#Link blocking
	elif (input == "link" or input == "link blocking"):
		embed=discord.Embed(title="Link Blocking",color=0xff8000)
		embed.add_field(name="Description", value="Deletes messages containing links. Won't delete messages by admins", inline=False)
		await bot.say(embed=embed)
	#Invite blocking
	elif (input == "invite" or input == "invite blocking"):
		embed=discord.Embed(title="Invite Blocking",color=0xff8000)
		embed.add_field(name="Description", value="Deletes messages containing discord server invites. Won't delete messages by admins", inline=False)
		await bot.say(embed=embed)
	#JoinDM
	elif (input == "joindm" or input == "join dm"):
		embed=discord.Embed(title="Join DM",color=0xff8000)
		embed.add_field(name="Description", value="Sends a message to users that join the server. The message can be set using `+config joindm <Join Message Text>`. Use `{user}` and `{server}` to put the users or servers name in.", inline=False)
		await bot.say(embed=embed)
	else:
		embed=discord.Embed(color=0xff8000)
		embed.add_field(name="Features", value="`join messages`, `leave messages`, `swear blocking`, `invite blocking`, `link blocking`, `Join DM`, and `self role setting`", inline=False)
		embed.add_field(name="Regular Commands", value="`+ping`, `+role`, `+report`", inline=False)
		embed.add_field(name="Moderator Commands", value="`+kick`, `+ban`, `+purge`", inline=False)
		embed.add_field(name="Administor Commands", value="`+config`, `+enable`, `+disable`, `+check`", inline=False)
		await bot.say(embed=embed)

# Kick user
@bot.command(pass_context=True)
async def kick(ctx, Member: discord.User):
	try:
		# Kicks user
		if (await check_config('kick', Member.server, False)):
			if (Member.id == "227422944123551754" or Member.id == "405829095054770187"):
				await bot.say("Unable to kick that user")
			else:
				if (ctx.message.server.me.server_permissions.kick_members or ctx.message.server.me.server_permissions.administrator):
					if (ctx.message.author.server_permissions.kick_members or ctx.message.author.server_permissions.administrator):
						if (ctx.message.author.top_role.position > Member.top_role.position):
							try:
								await bot.kick(Member)
								await bot.say("Successfully kicked **" + Member.name + "**")
							except discord.HTTPException:
								await bot.say("Unable to kick **" + Member.name + "**.")
						else:
							await bot.say("You do not have permission to kick** " + Member.name + "**")
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
# Ban user
@bot.command(pass_context=True)
async def ban(ctx, Member: discord.User, daysToDelete = 0):
	try:
		if (daysToDelete > 7 or daysToDelete < 0):
			await bot.say("You can only delete messages in days between 0 and 7")
			return
		if (await check_config('ban', Member.server, False)):
			if (Member.id == "227422944123551754" or Member.id == "405829095054770187"):
				await bot.say("Unable to ban that user")
			else:
				if (ctx.message.server.me.server_permissions.ban_members or ctx.message.server.me.server_permissions.administrator):
					if (ctx.message.author.server_permissions.ban_members or ctx.message.author.server_permissions.administrator):
						if (ctx.message.author.top_role.position > Member.top_role.position):
							try:
								await bot.ban(Member, delete_message_days=daysToDelete)
								await bot.say("Successfully banned **" + Member.name + "**")
							except discord.HTTPException:
								await bot.say("Unable to ban **" + Member.name + "**")
						else:
							await bot.say("You do not have permission to ban** " + Member.name + "**")
					else:
						await bot.say("You do not have permission to ban **" + Member.name + "**")
				else:
					await bot.say("Sorry, I do not have permission to ban.\nDisabling +ban now")
					await bot_disable(ctx.message.server, "ban")
		else:
			await bot.say("Ban is disabled")
	except:
		await bot.say("Error")
		print("Error")

# Sends a report to the report channel
@bot.command(pass_context=True)
async def report(ctx, Member: discord.User, *args):
	try:
		await bot.delete_message(ctx.message)
		if (await check_config('reportChannel', Member.server, True) == ''):
			await bot.say("No report channel has been setup")
		elif (await check_config('report', Member.server, False)):
			reportChannelBroken = False
			channelId = await check_config('reportChannel', Member.server, True)
			if "#" in channelId:
				channelId = channelId.replace('#', '')
				reportSendLocation = bot.get_channel(channelId)
				if (reportSendLocation == None):
					reportChannelBroken = True

			elif "@" in channelId:
				channelId = channelId.replace('@', '')
				try:
					reportSendLocation = await bot.get_user_info(channelId)
				except discord.NotFound:
					reportChannelBroken = True
			if (reportChannelBroken == False):
				await bot.send_message(ctx.message.author, "Your report against **"+Member.name+"#"+Member.discriminator+"** has been submitted")
				embed = discord.Embed(title="Submitted by "+ctx.message.author.name +
									  "#"+ctx.message.author.discriminator, description=' '.join(args))
				embed.set_author(name="Report against " +
								 Member.name+"#"+Member.discriminator)
				await bot.send_message(reportSendLocation, embed=embed)
			else:
				await bot.say("No report channel has been setup")
				await bot.send_message(ctx.message.author, "Your report against **"+Member.name+"#"+Member.discriminator+"** was unable to be submitted")
		else:
			await bot.say("Report is disabled")
	except:
		return
# Purges messages
@bot.command(pass_context=True)	 # Need to add perm checker
async def purge(ctx, numPurge: int, member: discord.Member = None):
	def predicate(msg: discord.Message) -> bool:
		return member is None or msg.author == member
	try:
		if (await check_config('purge', ctx.message.author.server, False)):
			if (ctx.message.server.me.server_permissions.manage_messages or ctx.message.server.me.server_permissions.administrator):
				if (ctx.message.author.server_permissions.manage_messages or ctx.message.author.server_permissions.administrator):
					if(numPurge >= 0 and numPurge <= 100):
						await bot.delete_message(ctx.message)
						try:
							await bot.purge_from(ctx.message.channel, limit=numPurge, check=predicate)
						except:
							await bot.say("Unable to purge messages")
					else:
						await bot.say("You can only purge up to 100 messages")
			else:
				await bot.say("Sorry, I do not have permission to delete messages. \nDisabling purge now")
				await bot_disable(ctx.message.server, "purge")
		else:
			await bot.say("Purge is disabled")
	except:
		await bot.say("Error")
		print("Error")

# Sets commands as enabled
@bot.command(pass_context=True)
async def enable(ctx, command: str):
	try:
		with open('config.json', 'r') as j:
			config = json.load(j)
			await update_data(config, ctx.message.server)
		if (ctx.message.author.server_permissions.administrator):
			#Ban
			if (command.lower() == "ban"):
				if (config[ctx.message.server.id]["enabled"]["ban"]==False):
					config[ctx.message.server.id]["enabled"]["ban"] = True
					await bot.say("Ban has been enabled")
				else:
					await bot.say("Ban was already enabled")
			#Kick
			elif (command.lower() == "kick"):
				if (config[ctx.message.server.id]["enabled"]["kick"]==False):
					config[ctx.message.server.id]["enabled"]["kick"] = True
					await bot.say("Kick has been enabled")
				else:
					await bot.say("Kick was already enabled")
			#Purge
			elif (command.lower() == "purge"):
				if (config[ctx.message.server.id]["enabled"]["purge"]==False):
					config[ctx.message.server.id]["enabled"]["purge"] = True
					await bot.say("Purge has been enabled")
				else:
					await bot.say("Purge was already enabled")
			#Join
			elif (command.lower() == "join"):
				if (config[ctx.message.server.id]["enabled"]["join"]==False):
					config[ctx.message.server.id]["enabled"]["join"] = True
					await bot.say("Join messages has been enabled")
				else:
					await bot.say("Join messages were already enabled")
			#Leave
			elif (command.lower() == "leave"):
				if (config[ctx.message.server.id]["enabled"]["leave"]==False):
					config[ctx.message.server.id]["enabled"]["leave"] = True
					await bot.say("Leave messages has been enabled")
				else:
					await bot.say("Leave messages were already enabled")
			#Report
			elif (command.lower() == "report"):
				if (config[ctx.message.server.id]["enabled"]["report"]==False):
					config[ctx.message.server.id]["enabled"]["report"] = True
					await bot.say("Reporting has been enabled")
				else:
					await bot.say("Reporting was already enabled")
			#Invite
			elif (command.lower() == "invite"):
				if (config[ctx.message.server.id]["enabled"]["invite"]==False):
					config[ctx.message.server.id]["enabled"]["invite"] = True
					await bot.say("Invite blocking has been enabled")
				else:
					await bot.say("Invite blocking was already enabled")
			#Swear
			elif (command.lower() == "swear"):
				if (config[ctx.message.server.id]["swear"]==0):
					config[ctx.message.server.id]["swear"]=1
				if (config[ctx.message.server.id]["enabled"]["swear"]==False):
					config[ctx.message.server.id]["enabled"]["swear"] = True
					await bot.say("Swear blocking has been enabled")
				else:
					await bot.say("Swear blocking was already enabled")
			#Role
			elif (command.lower() == "role"):
				if (config[ctx.message.server.id]["enabled"]["role"]==False):
					config[ctx.message.server.id]["enabled"]["role"] = True
					await bot.say("Self role setting has been enabled")
				else:
					await bot.say("Self role setting was already enabled")
			#Joindm
			elif (command.lower() == "joindm"):
				if (config[ctx.message.server.id]["enabled"]["joinDm"]==False):
					config[ctx.message.server.id]["enabled"]["joinDm"] = True
					await bot.say("Dm on join has been enabled")
				else:
					await bot.say("Dm on join was already enabled")
			#Link blocking
			elif (command.lower() == "link"):
				if (config[ctx.message.server.id]["enabled"]["link"]==False):
					config[ctx.message.server.id]["enabled"]["link"] = True
					await bot.say("Link blocking has been enabled")
				else:
					await bot.say("Link blocking was already enabled")
			else:
				await bot.say("Invalid argument. Do `+help enable` for more info")
		else:
			bot.say("You must have administrator to enable or disable a command")
		with open("config.json", "w") as j:
			json.dump(config, j, indent=4, sort_keys=True)
	except:
		await bot.say("Error")
		print("Error")

# Sets commands as disabled
@bot.command(pass_context=True)
async def disable(ctx, command: str):
	try:
		with open('config.json', 'r') as j:
			config = json.load(j)
			await update_data(config, ctx.message.server)
		if (ctx.message.author.server_permissions.administrator):
						#Ban
			if (command.lower() == "ban"):
				if (config[ctx.message.server.id]["enabled"]["ban"]==True):
					config[ctx.message.server.id]["enabled"]["ban"] = False
					await bot.say("Ban has been disabled")
				else:
					await bot.say("Ban was already disabled")
			#Kick
			elif (command.lower() == "kick"):
				if (config[ctx.message.server.id]["enabled"]["kick"]==True):
					config[ctx.message.server.id]["enabled"]["kick"] = False
					await bot.say("Kick has been disabled")
				else:
					await bot.say("Kick was already disabled")
			#Purge
			elif (command.lower() == "purge"):
				if (config[ctx.message.server.id]["enabled"]["purge"]==True):
					config[ctx.message.server.id]["enabled"]["purge"] = False
					await bot.say("Purge has been disabled")
				else:
					await bot.say("Purge was already disabled")
			#Join
			elif (command.lower() == "join"):
				if (config[ctx.message.server.id]["enabled"]["join"]==True):
					config[ctx.message.server.id]["enabled"]["join"] = False
					await bot.say("Join messages has been disabled")
				else:
					await bot.say("Join messages were already disabled")
			#Leave
			elif (command.lower() == "leave"):
				if (config[ctx.message.server.id]["enabled"]["leave"]==True):
					config[ctx.message.server.id]["enabled"]["leave"] = False
					await bot.say("Leave messages has been disabled")
				else:
					await bot.say("Leave messages were already disabled")
			#Report
			elif (command.lower() == "report"):
				if (config[ctx.message.server.id]["enabled"]["report"]==True):
					config[ctx.message.server.id]["enabled"]["report"] = False
					await bot.say("Reporting has been disabled")
				else:
					await bot.say("Reporting was already disabled")
			#Invite
			elif (command.lower() == "invite"):
				if (config[ctx.message.server.id]["enabled"]["invite"]==True):
					config[ctx.message.server.id]["enabled"]["invite"] = False
					await bot.say("Invite blocking has been disabled")
				else:
					await bot.say("Invite blocking was already disabled")
			#Swear
			elif (command.lower() == "swear"):
				if (config[ctx.message.server.id]["enabled"]["swear"]==True):
					config[ctx.message.server.id]["enabled"]["swear"] = False
					await bot.say("Swear blocking has been disabled")
				else:
					await bot.say("Swear blocking was already disabled")
			#Role
			elif (command.lower() == "role"):
				if (config[ctx.message.server.id]["enabled"]["role"]==True):
					config[ctx.message.server.id]["enabled"]["role"] = False
					await bot.say("Self role setting has been disabled")
				else:
					await bot.say("Self role setting was already disabled")
			#Joindm
			elif (command.lower() == "joindm"):
				if (config[ctx.message.server.id]["enabled"]["joinDm"]==True):
					config[ctx.message.server.id]["enabled"]["joinDm"] = False
					await bot.say("Dm on join has been disabled")
				else:
					await bot.say("Dm on join was already disabled")
			#Link blocking
			elif (command.lower() == "link"):
				if (config[ctx.message.server.id]["enabled"]["link"]==True):
					config[ctx.message.server.id]["enabled"]["link"] = False
					await bot.say("Link blocking has been disabled")
				else:
					await bot.say("Link blocking was already disabled")
			else:
				await bot.say("Invalid argument. Do `+help disable` for more info")
		else:
			bot.say("You must have administrator to set a command")
		with open("config.json", "w") as j:
			json.dump(config, j, indent=4, sort_keys=True)
	except:
		await bot.say("Error")
		print("Error")

# Sets commands
@bot.command(pass_context=True)
async def check(ctx):
	try:
		embed=discord.Embed(title="Check",color=0xff8000)

		# Join & Leave Messages
		joinLeaveCommands = ["Join", "Leave"]
		for i in joinLeaveCommands:
			if (await check_config(i.lower(), ctx.message.server, False)):
				cmdEnabled = "Enabled"
			else:
				cmdEnabled = "Disabled"
			embed.add_field(name=i + " messages", value=cmdEnabled, inline=False)

		# Kick Ban Purge & Report
		basicCommands = ["Kick", "Ban", "Purge", "Report"]
		for i in basicCommands:
			if (await check_config(i.lower(), ctx.message.server, False)):
				cmdEnabled = "Enabled"
			else:
				cmdEnabled = "Disabled"
			embed.add_field(name=i, value=cmdEnabled, inline=False)
		
		# JoinDm
		if (await check_config('joinDm', ctx.message.server, False)):
			cmdEnabled = "Enabled"
		else:
			cmdEnabled = "Disabled"
		embed.add_field(name="JoinDm", value=cmdEnabled, inline=False)
		
		# Invite Blocking
		if (await check_config('invite', ctx.message.server, False)):
			cmdEnabled = "Enabled"
		else:
			cmdEnabled = "Disabled"
		embed.add_field(name="Invite Blocking", value=cmdEnabled, inline=False)

		# Link Blocking
		if (await check_config('link', ctx.message.server, False)):
			cmdEnabled = "Enabled"
		else:
			cmdEnabled = "Disabled"
		embed.add_field(name="Link Blocking", value=cmdEnabled, inline=False)

		# Swear Blocking
		if (await check_config('swear', ctx.message.server, False)):
			cmdEnabled = "Enabled"
		else:
			cmdEnabled = "Disabled"
		cmd2Enabled = await check_config('swear', ctx.message.server, True)
		embed.add_field(name="Swear Blocking", value=cmdEnabled+" and is set to "+str(cmd2Enabled), inline=False)

		# Self role setting
		if (await check_config("role", ctx.message.server, False)):
			cmdEnabled = "Enabled"
		else:
			cmdEnabled = "Disabled"
		embed.add_field(name="Self role setting", value=cmdEnabled, inline=False)

		# Channels for admins
		if (ctx.message.author.server_permissions.administrator):
			# Report channel
			reportChannelBroken = False
			channelId = await check_config('reportChannel', ctx.message.server, True)
			if (await check_config('report', ctx.message.server, False)):
				if "#" in channelId:
					channelId = channelId.replace('#', '')
					reportSendLocation = bot.get_channel(channelId)
					if (reportSendLocation != None):
						embed.add_field(name="Report channel", value=reportSendLocation.mention,inline=False)
					else:
						embed.add_field(name="Report channel", value="**Not setup**", inline=False)

				elif "@" in channelId:
					channelId = channelId.replace('@', '')
					try:
						reportSendLocation = await bot.get_user_info(channelId)
					except discord.NotFound:
						reportChannelBroken = True

					if(reportChannelBroken == False):
						embed.add_field(name="Report channel", value=reportSendLocation.name+"#"+reportSendLocation.discriminator,inline=False)
					else:
						embed.add_field(name="Report channel", value="**Not setup**", inline=False)
				else:
					embed.add_field(name="Report channel", value="**Not setup**", inline=False)

			# Joinleave channel
			channel = await check_config('joinleaveChannel', ctx.message.server, True)
			if channel == "":
				embed.add_field(name="Join/leave Message Channel", value="**Not setup**", inline=False)
			else:
				joinleaveChannel = bot.get_channel(channel)
				embed.add_field(name="Join/leave Message Channel", value=joinleaveChannel.mention, inline=False)
				
			# Join Leave Text
			joinMsgText = await check_config('joinMsgText', ctx.message.server, True)
			if (joinMsgText == ""):
				joinMsgText = "Welcome {user}"
			embed.add_field(name="Join Message Text", value='`'+joinMsgText+'`', inline=False)

			leaveMsgText = await check_config('leaveMsgText', ctx.message.server, True)
			if (leaveMsgText == ""):
				leaveMsgText = "{user} has left the server"
			embed.add_field(name="Leave Message Text", value='`'+leaveMsgText+'`', inline=False)
			
			# Joindm text
			joinDmText = (await check_config('joinDmText', ctx.message.server, True))
			if joinDmText == "":
				embed.add_field(name="Join DM Text", value='**Not setup**', inline=False)
			else:
				embed.add_field(name="Join DM Text", value='`'+joinDmText+'`', inline=False)
		await bot.say(embed=embed)

	except:
		await bot.say("Error getting server settings")

# Sets commands
@bot.command(pass_context=True)
async def config(ctx, command: str, *args):
	try:
		if (len(args)>0):
			input = args[0]
		with open('config.json', 'r') as j:
			config = json.load(j)
			await update_data(config, ctx.message.server)

		if (ctx.message.author.server_permissions.administrator):
			#Join/leave channel
			if (command.lower() == 'join' or command.lower() == 'leave' or command.lower() == 'joinleave'):
				channelId = input.replace('#', '').replace('<', '').replace('>', '')

				if (bot.get_channel(channelId) == None):
					await bot.say("Not a valid channel")
				else:
					await bot.say("Set join & leave messages channel to "+input)
					config[ctx.message.server.id]["joinleaveChannel"] = channelId
			#Report channel
			elif (command.lower() == 'report'):
				channelId = input.replace('<', '').replace('>', '').replace('!', '')
				if (bot.get_channel(channelId.replace('#', '')) == None):
					invalidChannel = False
					try:
						await bot.get_user_info(channelId.replace('@', ''))
					except discord.NotFound:
						invalidChannel = True
				else:
					invalidChannel = False

				if (invalidChannel == False):
					await bot.say("Set report messages channel to "+input)
					config[ctx.message.server.id]["reportChannel"] = channelId
				else:
					await bot.say("Invalid channel name")
			#Swear blocking level
			elif (command.lower() == 'swear'):
				if (int(input) >= 0 and int(input) <= 3):
					config[ctx.message.server.id]["swear"] = int(input)
					await bot.say("Set swear blocking level to "+input)
				elif (int(input)):
					config[ctx.message.server.id]["enabled"]["swear"] = 0
					await bot_disable(ctx.message.server, 'swear')
					await bot.say("Disabled swear blocking")
				else:
					await bot.say("Invalid level, must be between 0-3")
			#Roles
			elif (command.lower() == 'role'or command.lower() == 'roles'):
				setRoles = " ".join(args).split(';')
				for i in setRoles:
					role = discord.utils.get(ctx.message.server.roles, name=i)
					if (role == None)or(setRoles.count(i) > 1)or(role.position >= ctx.message.author.top_role.position)or(role.managed):
						await bot.say("Invalid role(s)")
						return
					elif (role.position > ctx.message.server.me.top_role.position):
						await bot.say("Unable to set, one or more of the roles is above my highest role")
						return
				a = 0
				for i in setRoles:
					role = discord.utils.get(ctx.message.server.roles, name=i)
					setRoles[a] = role.id
					a = a+1
				with open('config.json', 'r') as j:
					config = json.load(j)
					await update_data(config, ctx.message.server)
				config[ctx.message.server.id]["role"] = setRoles
				with open("config.json", "w") as j:
					json.dump(config, j, indent=4, sort_keys=True)
				await bot.say("Succesfully set roles")
			#Join dm
			elif (command.lower() == 'joindm'):
				if (len(" ".join(args)) <= 200):
					config[ctx.message.server.id]["joinDmText"] = " ".join(args).replace('\\n', '\n')
					await bot.say("Join dm message set to ```"+config[ctx.message.server.id]["joinDmText"]+"\n```")
				else:
					await bot.say("Too many characters, max 200")
					return
			#Join Message
			elif (command.lower() == 'joinmsg'):
				if (len(" ".join(args)) <= 200):
					config[ctx.message.server.id]["joinMsgText"] = " ".join(args).replace('\\n', '\n')
					await bot.say("Join message set to ```"+config[ctx.message.server.id]["joinMsgText"]+"\n```")
				else:
					await bot.say("Too many characters, max 200")
					return
			#Leave message
			elif (command.lower() == 'leavemsg'):
				if (len(" ".join(args)) <= 200):
					config[ctx.message.server.id]["leaveMsgText"] = " ".join(args).replace('\\n', '\n')
					await bot.say("Leave message set to ```"+config[ctx.message.server.id]["leaveMsgText"]+"\n```")
				else:
					await bot.say("Too many characters, max 200")
					return
			#Clear config
			elif (command.lower() == 'clear'):
				await bot.say("Are you sure you want to clear this my config for this server? Type `confirm` if you're sure")
				msg = await bot.wait_for_message(timeout=20, author=ctx.message.author,content='confirm')
				if(msg!=None):
					del config[ctx.message.server.id]
					await bot.say("Cleared this server's config")
				else:
					await bot.say("Config clear timed out")
			else:
				await bot.say("Invalid argument. Do `+help set` for more info")
		else:
			bot.say("You must have administrator to configure a command")
		with open("config.json", "w") as j:
			json.dump(config, j, indent=4, sort_keys=True)
	except discord.HTTPException:
		await bot.say("Error")
		print("Error")

#Check latency of bot
@bot.command(pass_context=True)
async def ping(ctx):
    t = await bot.say('Pong!')
    ms = (t.timestamp-ctx.message.timestamp).total_seconds() * 1000
    await bot.edit_message(t, new_content='Pong! Took: {}ms'.format(int(ms)))
		
# Allows users to set their own roles
@bot.command(pass_context=True)
async def role(ctx, *args):
	if (await check_config('role', ctx.message.author.server, False)):
		if str(args) == "()":
			roleList = await check_config('role', ctx.message.server, True)
			a = 0
			for i in roleList:
				role = discord.utils.get(ctx.message.server.roles, id=i)
				roleList[a] = str(role)
				a += 1
			if None in roleList:
				await bot.say("Unable to find roles, try `+config role` to reset them")
			elif len(roleList) == 0:
				await bot.say("No roles have been set using `+config role`\nDisabling +role now")
				await bot_disable(ctx.message.server, 'role')
			else:
				await bot.say("You can set your roles to the following: `"+'`, `'.join(roleList)+"`")
			return
		role = discord.utils.get(ctx.message.server.roles, name=" ".join(args))
		if (role != None):
			roleList = await check_config('role', ctx.message.server, True)
			a = 0
			for i in roleList:
				role = discord.utils.get(ctx.message.server.roles, id=i)
				roleList[a] = str(role)
				a += 1
			if None in roleList:
				await bot.say("Unable to find roles, try `+config roles` to reset them")
			role = discord.utils.get(
				ctx.message.server.roles, name=" ".join(args))
			if str(role) in (roleList):
				if (role.position < ctx.message.server.me.top_role.position):
					if role not in ctx.message.author.roles:
						try:
							await bot.add_roles(ctx.message.author, role)
							await bot.say("Added you to the `"+role.name+"` role")
						except:
							await bot.say("Error")
					elif role in ctx.message.author.roles:
						await bot.remove_roles(ctx.message.author, role)
						await bot.say("Removed you from the `"+role.name+"` role")
				else:
					await bot.say("Sorry, I do not have permission to set roles.\nDisabling +role now")
					await bot_disable(ctx.message.server, 'role')
			else:
				await bot.say("That is not a valid role")
		else:
			await bot.say("Unable to find that role")
	else:
		await bot.say("Role setting is disabled")

# Function to disable bot commands serverside


async def bot_disable(server, command):
	with open('config.json', 'r') as j:
		config = json.load(j)
		await update_data(config, server)
	config[server.id]["enabled"][command] = False
	with open("config.json", "w") as j:
		json.dump(config, j, indent=4, sort_keys=True)

# Function to update json file
async def update_data(config, server):
	if not server.id in config:
		config[server.id] = {}
		config[server.id]["enabled"] = {}
		config[server.id]["enabled"]['join'] = True
		config[server.id]["enabled"]['leave'] = True
		config[server.id]["enabled"]['kick'] = True
		config[server.id]["enabled"]['ban'] = True
		config[server.id]["enabled"]['purge'] = True
		config[server.id]["enabled"]['report'] = False
		config[server.id]["enabled"]['invite'] = False
		config[server.id]["enabled"]['swear'] = True
		config[server.id]["enabled"]['role'] = False
		config[server.id]["enabled"]['joinDm'] = False
		config[server.id]["enabled"]['link'] = False
		config[server.id]['swear'] = 1
		config[server.id]["joinleaveChannel"] = ""
		config[server.id]["reportChannel"] = ""
		config[server.id]["joinDmText"] = ""
		config[server.id]["joinMsgText"] = ""
		config[server.id]["leaveMsgText"] = ""
		config[server.id]["role"] = []
	
# Function to make it easier for commands to check their config
async def check_config(command, server, outsideEnabled):
	try:
		with open('config.json', 'r') as j:
			config = json.load(j)
		await update_data(config, server)
		if (outsideEnabled == False):
			return config[server.id]["enabled"][command]
		else:
			return config[server.id][command]
	except:
		return

# Opens words file
if (os.path.exists('words') == False):
	os.mkdir('words')
i = 1
while (i <= 3):
	if (os.path.exists('words/words'+str(i)+'.txt') == False):
		open('words/words'+str(i)+'.txt', "w")
	i += 1

if (os.path.exists('config.json') == False):
	config = {}
	with open("config.json", "w") as j:
		json.dump(config, j)

if (os.path.exists('key.config') == False):
	open('key.config', "w")
	print("Unable to run litebot, add your key to key.config")
	quit()
words1 = open('words/words1.txt', 'r').read().lower().splitlines()
words2 = open('words/words2.txt', 'r').read().lower().splitlines()
words3 = open('words/words3.txt', 'r').read().lower().splitlines()

# Bot Token
bot.run(open('key.config', 'r').read())
