import discord
import json
import os
import sys
from datetime import datetime
from discord.ext import commands
from discord.ext.commands import Bot

print ('Lite-Bot is activating')

bot=Bot(command_prefix="!")
#prefix is !

bot.remove_command('help')
@bot.event
async def on_ready():
	print ('Ready\n')
	print("       _             ")
	print("   .__(.)< (MEOW)    ")
	print("   \___)             ")
	print("~~~~~~~~~~~~~~~~~~~~~")
	updateConsole()

@bot.async_event
async def on_server_join(Server : discord.Server):
	updateConsole()
			
@bot.async_event
async def on_server_remove(Server : discord.Server):
	updateConsole()
			
def updateConsole():
	print("{members} users in {servers} servers".format(members=str(len(set(bot.get_all_members()))-1),servers=str(len(bot.servers))),end='\r')
	with open('servers.txt', 'w') as f:
		for item in bot.servers:
			f.write("%s\n" % item)

#Message on user join
@bot.async_event
async def on_member_join(Member : discord.User):
	try:
		#Join message
		if (await check_config('join',Member.server, False)==1):
			channel = bot.get_channel(await check_config('joinleaveChannel',Member.server, True))
			joinMsgText = await check_config('joinMsgText',Member.server, True)
			if joinMsgText=="":
				joinMsgText="Welcome {user}"
			if (channel!=None):
				await bot.send_message(channel,joinMsgText.format(user=Member.mention,server=Member.server.name))

		#Join dm
		if (await check_config('joinDm',Member.server, False)==1):
			dmText = (await check_config('joinDmText',Member.server, True))
			if (dmText==""):
				return
			elif (len(dmText)>=200):
				return
			await bot.send_message(Member,dmText.format(user=Member.mention,server=Member.server.name))
		updateConsole()
	except:
		print("Error")

#Message on user leave
@bot.async_event
async def on_member_remove(Member : discord.User):
	try:
		if (await check_config('leave',Member.server, False)==1):
			channel = bot.get_channel(await check_config('joinleaveChannel',Member.server, True))
			leaveMsgText = await check_config('leaveMsgText',Member.server, True)
			if leaveMsgText=="":
				leaveMsgText="{user} has left the server"
			if (channel!=None):
				await bot.send_message(channel,leaveMsgText.format(user=Member.name,server=Member.server.name))
		updateConsole()
	except:
		print("Error")

#Deletes messages that include key words, and discord invites
@bot.event
async def on_message(message, timeout=10):
	await bot.change_presence(game=discord.Game(name='Protecting the Server | !help'))

	unableToCheckMessages=False
	if (message.channel.is_private==False and message.author!=message.server.me):
		if (await check_config('swear', message.author.server, False) >=1):
			if (message.server.me.server_permissions.manage_messages  or message.server.me.server_permissions.administrator):
				toDelete=False

				for i in words1:
					if ((str(i) in message.content.lower()) and (await check_config('swear', message.author.server, False) >=1)):
						toDelete=True

				for i in words2:
					if ((str(i) in message.content.lower()) and (await check_config('swear', message.author.server, False) >=2)):
						toDelete=True

				for i in words3:
					if ((str(i) in message.content.lower()) and (await check_config('swear', message.author.server, False) >=3)):
						toDelete=True

				if toDelete:
					await bot.delete_message(message)
					await bot.send_message(message.channel, "No swearing")
					return
			else:
				unableToCheckMessages=True
		if ((await check_config('invite',message.author.server, False)==1)and(message.author.server_permissions.administrator==False)):
			if (message.server.me.server_permissions.manage_messages  or message.server.me.server_permissions.administrator):
				if ("discord.gg" in message.content.lower()):
					await bot.delete_message(message)
					await bot.send_message(message.channel, "Invites are not allowed in this server")
					return
			else:
				unableToCheckMessages=True

		if (unableToCheckMessages):
			try:
				await bot_disable(message.server, 'swear')
				await bot_disable(message.server, 'invite')
				await bot.send_message(message.channel,"Unable to check messages as I do not have permission to delete messages.\nDisabling Swear Blocking and Invite Blocking now")
				unableToCheckMessages=False
			except:
				return
		await bot.process_commands(message)
		
		if ("<@405829095054770187>" in message.content)and("!purge" not in message.content):
			await bot.send_message(message.channel, "Hi, I'm lite-bot, a administrative bot designed to make running a server easier. My prefix is `!` and you can see my commands using `!help`")
			return
		runOnce=False
		async for message in bot.logs_from(message.channel,limit=2):
			if runOnce==False:
				if ("stfu" in message.content.lower())or("die" in message.content.lower())or("kys" in message.content.lower()):
					sayNo=True
				else:
					sayNo=False
				runOnce=True
			else:
				if (message.author == bot.user)and sayNo:
					await bot.send_message(message.channel,"No")
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
		if ("".join(args)=="kick"):
			await bot.sayd	("Kicks an user\n`!kick @user#0000`")
		elif ("".join(args)=="ban"):
			await bot.say("Bans an user and deletes their messages from the past 3 days\n`!ban @user#0000`")
		elif ("".join(args)=="purge"):
			await bot.say("Mass deletes messages, can also purge a specific user\n`!purge 30 @user#0000`")
		elif ("".join(args)=="report"):
			await bot.say("Sends a report to the server\n`!report @user#0000 Stealing the Village gold`")
		elif ("".join(args)=="config"):
			await bot.say("Sets a `role`, `swear`, `joinleave`, `joindm`, `joinmsg`, or `leavemsg` to a value, use `;` to seperate values\n `!set joinleave #general`")
		elif ("".join(args)=="enable"or"".join(args)=="disable"):
			await bot.say("Enables or disables a command\n `!enable kick`")
		elif ("".join(args)=="check"):
			await bot.say("Checks what the server config is set to\n `!check`")
		elif ("".join(args)=="role"):
			await bot.say("Sets you to a role\n `!role role1`")
		else:
			embed=discord.Embed(title="Help")
			embed.add_field(name="!kick", value="!kick @user#0000", inline=False)
			embed.add_field(name="!ban", value="!ban @user#0000", inline=False)
			embed.add_field(name="!purge", value="!purge <NumberOfMessages>", inline=False)
			embed.add_field(name="!report", value="!report @user#0000 \"Report Content\"", inline=False)
			embed.add_field(name="!role", value="!role <role name>", inline=False)
			embed.add_field(name="!check", value="!check", inline=False)
			if(ctx.message.author.server_permissions.administrator):
				embed.add_field(name="!enable", value="!enable <kick>", inline=False)
				embed.add_field(name="!disable", value="!disable <command>", inline=False)
				embed.add_field(name="!config", value="!set <command> <channel>", inline=False)
			await bot.say(embed=embed)
	except:
		await bot.say("Error")
		print("Error")
#Kick user
@bot.command (pass_context=True)
async def kick(ctx, Member : discord.User):
	try:
		if (await check_config('kick',Member.server, False)==1):
			if (Member.id=="227422944123551754" or Member.id=="405829095054770187"):
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
#Ban user
@bot.command (pass_context=True)
async def ban(ctx, Member : discord.User):
	try:
		if (await check_config('ban',Member.server, False)==1):
			if (Member.id=="227422944123551754" or Member.id=="405829095054770187"):
				await bot.say("Unable to ban that user")
			else:
				if (ctx.message.server.me.server_permissions.ban_members or ctx.message.server.me.server_permissions.administrator):
					if (ctx.message.author.server_permissions.ban_members  or ctx.message.author.server_permissions.administrator):
						if (ctx.message.author.top_role.position > Member.top_role.position):
							try:
								await bot.ban(Member, delete_message_days=3)
								await bot.say("Successfully banned **" + Member.name + "**")
							except discord.HTTPException:
								await bot.say("Unable to ban **" + Member.name + "**")
						else:
							await bot.say("You do not have permission to ban** " + Member.name + "**")
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
async def report(ctx, Member : discord.User, *args):
	try:
		if ((await check_config('report',Member.server, False)==1)and(await check_config('reportChannel',Member.server, True) !='')):
			reportChannelBroken = False
			channelId=await check_config('reportChannel',Member.server, True)
			if "#" in channelId:
				channelId=channelId.replace('#', '')
				reportSendLocation=bot.get_channel(channelId)
				if (reportSendLocation==None):
					reportChannelBroken = True

			elif "@" in channelId:
				channelId=channelId.replace('@', '')
				try:
					reportSendLocation=await bot.get_user_info(channelId)
				except discord.NotFound:
					reportChannelBroken = True
			if (reportChannelBroken==False):
				await bot.send_message(ctx.message.author, "Your report against **"+Member.name+"#"+Member.discriminator+"** has been submitted")
				await bot.delete_message(ctx.message)
				embed=discord.Embed(title="Submitted by "+ctx.message.author.name+"#"+ctx.message.author.discriminator, description=' '.join(args))
				embed.set_author(name="Report against "+Member.name+"#"+Member.discriminator)
				await bot.send_message(reportSendLocation, embed=embed)
			else:
				print("Gotten Here")
				await bot.delete_message(ctx.message)
				await bot.send_message(ctx.message.author, "Your report against **"+Member.name+"#"+Member.discriminator+"** was unable to be submitted")
		else:
			await bot.say("Report is disabled")
	except:
		return
#Purges messages
@bot.command (pass_context=True)#Need to add perm checker
async def purge(ctx, numPurge: int, member: discord.Member = None):
	def predicate(msg: discord.Message) -> bool:
		return member is None or msg.author == member
	try:
		if (await check_config('purge',ctx.message.author.server, False)==1):
			if (ctx.message.server.me.server_permissions.manage_messages or ctx.message.server.me.server_permissions.administrator):
				if (ctx.message.author.server_permissions.manage_messages or ctx.message.author.server_permissions.administrator):
					if(numPurge >=0 and numPurge <=100):
						await bot.delete_message(ctx.message)
						try:
							await bot.purge_from(ctx.message.channel,limit=numPurge,check=predicate)
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

#Sets commands as enabled
@bot.command (pass_context=True)
async def enable(ctx, command : str):
	try:
		with open('config.json', 'r') as j:
			config=json.load(j)
			await update_data(config, ctx.message.server)
		if (ctx.message.author.server_permissions.administrator):
			if (command=="ban"):
				config[ctx.message.server.id]["enabled"]["ban"]=1
				await bot.say("Ban has been enabled")
			elif (command.lower()=='kick'):
				config[ctx.message.server.id]["enabled"]['kick']=1
				await bot.say("Kick has been enabled")
			elif (command.lower()=='purge'):
				config[ctx.message.server.id]["enabled"]['purge']=1
				await bot.say("Purge has been enabled")
			elif (command.lower()=='join'):
				config[ctx.message.server.id]["enabled"]['join']=1
				await bot.say("Join messages has been enabled")
			elif (command.lower()=='leave'):
				config[ctx.message.server.id]["enabled"]['leave']=1
				await bot.say("Leave messages has been enabled")
			elif (command.lower()=='report'):
				config[ctx.message.server.id]["enabled"]['report']=1
				await bot.say("Reporting has been enabled")
			elif (command.lower()=='invite'):
				config[ctx.message.server.id]["enabled"]['invite']=1
				await bot.say("Invite blocking has been enabled")
			elif (command.lower()=='swear'):
				config[ctx.message.server.id]["enabled"]['swear']=1
				await bot.say("Swear blocking has been enabled")
			elif (command.lower()=='role'):
				config[ctx.message.server.id]["enabled"]['role']=1
				await bot.say("Self role setting has been enabled")
			elif (command.lower()=='joindm'):
				config[ctx.message.server.id]["enabled"]['joinDm']=1
				await bot.say("Dm on join has been enabled")
			else:
				await bot.say("Invalid argument. Do `!help enable` for more info")
		else:
			bot.say("You must have administrator to enable or disable a command")
		with open("config.json", "w") as j:
			json.dump(config, j, indent=4, sort_keys=True)
	except:
		await bot.say("Error")
		print("Error")

#Sets commands as disabled
@bot.command (pass_context=True)
async def disable(ctx, command : str):
	try:
		with open('config.json', 'r') as j:
			config=json.load(j)
			await update_data(config, ctx.message.server)
		if (ctx.message.author.server_permissions.administrator):
			if (command=="ban"):
				config[ctx.message.server.id]["enabled"]["ban"]=0
				await bot.say("Ban has been disabled")
			elif (command.lower()=='kick'):
				config[ctx.message.server.id]["enabled"]['kick']=0
				await bot.say("Kick has been disabled")
			elif (command.lower()=='purge'):
				config[ctx.message.server.id]["enabled"]['purge']=0
				await bot.say("Purge has been disabled")
			elif (command.lower()=='join'):
				config[ctx.message.server.id]["enabled"]['join']=0
				await bot.say("Join messages has been disabled")
			elif (command.lower()=='leave'):
				config[ctx.message.server.id]["enabled"]['leave']=0
				await bot.say("Leave messages has been disabled")
			elif (command.lower()=='report'):
				config[ctx.message.server.id]["enabled"]['report']=0
				await bot.say("Reporting has been disabled")
			elif (command.lower()=='invite'):
				config[ctx.message.server.id]["enabled"]['invite']=0
				await bot.say("Invite blocking has been disabled")
			elif (command.lower()=='swear'):
				config[ctx.message.server.id]["enabled"]['swear']=0
				await bot.say("Swear blocking has been disabled")
			elif (command.lower()=='role'):
				config[ctx.message.server.id]["enabled"]['role']=0
				await bot.say("Self role setting has been disabled")
			elif (command.lower()=='joindm'):
				config[ctx.message.server.id]["enabled"]['joinDm']=0
				await bot.say("Dm on join has been disabled")
			else:
				await bot.say("Invalid argument. Do `!help disable` for more info")
		else:
			bot.say("You must have administrator to set a command")
		with open("config.json", "w") as j:
			json.dump(config, j, indent=4, sort_keys=True)
	except:
		await bot.say("Error")
		print("Error")

#Sets commands
@bot.command (pass_context=True)
async def check(ctx):
	try:
		checkString=""

		#Join & Leave Messages
		joinLeaveCommands=["Join", "Leave"]
		for i in joinLeaveCommands:
			if (await check_config(i.lower(),ctx.message.server, False)==1):
				cmdEnabled="Enabled"
			else:
				cmdEnabled="Disabled"
			stringAddition=(i +" messages are **"+cmdEnabled+"**\n")
			checkString=checkString + stringAddition

		#Kick Ban Purge & Report
		basicCommands=["Kick","Ban","Purge","Report","JoinDm"]
		for i in basicCommands:
			if (await check_config(i.lower(),ctx.message.server, False)==1):
				cmdEnabled="Enabled"
			else:
				cmdEnabled="Disabled"
			stringAddition=(i +" is **"+cmdEnabled+"**\n")
			checkString=checkString + stringAddition

		#Invite Blocking
		if (await check_config('invite',ctx.message.server, False)==1):
			cmdEnabled="Enabled"
		else:
			cmdEnabled="Disabled"
		stringAddition=("Invite blocking is **"+cmdEnabled+"**\n")
		checkString=checkString + stringAddition

		#Swear Blocking
		cmd2Enabled=await check_config('swear',ctx.message.server, False)
		swearEnabled=("Swear blocking is set to **"+str(cmd2Enabled)+"**\n")
		checkString=checkString + swearEnabled

		#Self role setting
		if (await check_config("role",ctx.message.server, False)==1):
			cmdEnabled="Enabled"
		else:
			cmdEnabled="Disabled"
		stringAddition=("Self role setting is **"+cmdEnabled+"**")
		checkString=checkString + stringAddition

		await bot.say(checkString)
		#Channels for admins
		if (ctx.message.author.server_permissions.administrator):
			ChannelString=""

			#Report channel
			reportChannelBroken=False
			channelId=await check_config('reportChannel',ctx.message.server, True)
			if "#" in channelId:
				channelId=channelId.replace('#', '')
				reportSendLocation=bot.get_channel(channelId)
				if (reportSendLocation!=None):
					ChannelString=("Report channel is set to "+reportSendLocation.mention)
				else:
					ChannelString=("Report channel is **not setup**")

			elif "@" in channelId:
				channelId=channelId.replace('@', '')
				try:
					reportSendLocation=await bot.get_user_info(channelId)
				except discord.NotFound:
					reportChannelBroken = True

				if(reportChannelBroken==False):
					ChannelString=("Report channel is set to **"+reportSendLocation.name+"#"+reportSendLocation.discriminator+"**")
				else:
					ChannelString=("Report channel is **not setup**")
			else:
				ChannelString=("Report channel is **not setup**")

			#Joinleave channel
			channel=await check_config('joinleaveChannel',ctx.message.server, True)
			if channel=="":
				ChannelString=ChannelString + "\nJoin/Leave message channel is **not setup**"
			else:
				joinleaveChannel=bot.get_channel(channel)
				ChannelString=ChannelString + "\nJoin/Leave message channel is set to "+joinleaveChannel.mention
			#Join Leave Text
			joinMsgText = await check_config('joinMsgText',ctx.message.server, True)
			if (joinMsgText==""):
				joinMsgText="Welcome {user}"
			ChannelString=ChannelString+"\nJoin messages text is set to: \n```"+joinMsgText+"```"

			leaveMsgText = await check_config('leaveMsgText',ctx.message.server, True)
			if (leaveMsgText==""):
				leaveMsgText="{user} has left the server"
			ChannelString=ChannelString+"\nLeave messages text is set to: \n```"+leaveMsgText+"```"
			#Joindm text
			joinDmText = (await check_config('joinDmText',ctx.message.server, True))
			if joinDmText=="":
				ChannelString=ChannelString + "\nJoin Dm message text is **not set up**"
			else:
				ChannelString=ChannelString + "\nJoin Dm message text is set to: \n```"+joinDmText+"```"
			await bot.say(ChannelString)

	except:
		await boy.say("Error getting server settings")

#Sets commands
@bot.command (pass_context=True)
async def config(ctx, command : str, *args):
	try:
		input = args[0]
		with open('config.json', 'r') as j:
			config=json.load(j)
			await update_data(config, ctx.message.server)

		if (ctx.message.author.server_permissions.administrator):

			if (command.lower()=='join' or command.lower()=='leave' or command.lower()=='joinleave'):
				channelId=input.replace('#', '').replace('<', '').replace('>', '')

				if (bot.get_channel(channelId)==None):
					await bot.say("Not a valid channel")
				else:
					await bot.say("Set join & leave messages channel to "+input)
					config[ctx.message.server.id]["joinleaveChannel"]=channelId

			elif (command.lower()=='report'):
				channelId=input.replace('<', '').replace('>', '').replace('!', '')
				if (bot.get_channel(channelId.replace('#', ''))==None):
					invalidChannel=False
					try:
						await bot.get_user_info(channelId.replace('@', ''))
					except discord.NotFound:
						invalidChannel=True
				else:
					invalidChannel=False

				if (invalidChannel==False):
					await bot.say("Set report messages channel to "+input)
					config[ctx.message.server.id]["reportChannel"]=channelId
				else:
					await bot.say("Invalid channel name")

			elif (command.lower()=='swear'):
				if (int(input)>=0 and int(input)<=3):
					config[ctx.message.server.id]["enabled"]["swear"]=int(input)
					await bot.say("Set swear blocking level to "+input)
				else:
					await bot.say("Invalid level, must be between 0-3")

			elif (command.lower()=='role'or command.lower()=='roles'):
				setRoles=" ".join(args).split(';')
				for i in setRoles:
					role=discord.utils.get(ctx.message.server.roles, name=i)
				if (role==None)or(setRoles.count(i)>1)or(role.position >= ctx.message.author.top_role.position)or(role.managed):
					await bot.say("Invalid role(s)")
					return
				elif (role.position > ctx.message.server.me.top_role.position):
					await bot.say("Unable to set, one or more of the roles is above my highest role")
					return
				a=0
				for i in setRoles:
					role=discord.utils.get(ctx.message.server.roles, name=i)
					setRoles[a]=role.id
					a=a+1
				with open('config.json', 'r') as j:
					config=json.load(j)
					await update_data(config, ctx.message.server)
				config[ctx.message.server.id]["role"]=setRoles
				with open("config.json", "w") as j:
					json.dump(config, j, indent=4, sort_keys=True)
				await bot.say("Succesfully set roles")

			elif (command.lower()=='joindm'):
				if (len(" ".join(args))<=200):
					config[ctx.message.server.id]["joinDmText"]=" ".join(args).replace('\\n','\n')
					await bot.say("Join dm message set to ```"+config[ctx.message.server.id]["joinDmText"]+"```")
				else:
					await bot.say("Too many characters, max 200")
					return

			elif (command.lower()=='joinmsg'):
				if (len(" ".join(args))<=200):
					config[ctx.message.server.id]["joinMsgText"]=" ".join(args).replace('\\n','\n')
					await bot.say("Join message set to ```"+config[ctx.message.server.id]["joinMsgText"]+"```")
				else:
					await bot.say("Too many characters, max 200")
					return

			elif (command.lower()=='leavemsg'):
				if (len(" ".join(args))<=200):
					config[ctx.message.server.id]["leaveMsgText"]=" ".join(args).replace('\\n','\n')
					await bot.say("Leave message set to ```"+config[ctx.message.server.id]["leaveMsgText"]+"```")
				else:
					await bot.say("Too many characters, max 200")
					return

			else:
				await bot.say("Invalid argument. Do `!help set` for more info")
		else:
			bot.say("You must have administrator to enable or disable a command")
		with open("config.json", "w") as j:
			json.dump(config, j, indent=4, sort_keys=True)
	except discord.HTTPException:
		await bot.say("Error")
		print("Error")

#Allows users to set their own roles
@bot.command (pass_context=True)
async def role(ctx, *args):
	if (await check_config('role',ctx.message.author.server, False)==1):
		if str(args)=="()":
			roleList=await check_config('role',ctx.message.server, True)
			a=0
			for i in roleList:
				role=discord.utils.get(ctx.message.server.roles, id=i)
				roleList[a]=str(role)
				a+=1
			if None in roleList:
				await bot.say("Unable to find roles, try `!setroles` to reset them")
			elif len(roleList) == 0:
				await bot.say("No roles have been set using `!setroles`\nDisabling !role now")
				await bot_disable(ctx.message.server, 'role')
			else:
				await bot.say("You can set your roles to the following: `"+'`, `'.join(roleList)+"`")
			return
		role=discord.utils.get(ctx.message.server.roles, name=" ".join(args))
		if (role !=None):
			roleList=await check_config('role',ctx.message.server, True)
			a=0
			for i in roleList:
				role=discord.utils.get(ctx.message.server.roles, id=i)
				roleList[a]=str(role)
				a+=1
			if None in roleList:
				await bot.say("Unable to find roles, try `!setroles` to reset them")
			role=discord.utils.get(ctx.message.server.roles, name=" ".join(args))
			if str(role) in (roleList):
				if (role.position < ctx.message.server.me.top_role.position):
					if role not in ctx.message.author.roles:
						try:
							await bot.add_roles(ctx.message.author, role)
							await bot.say("Successfully gave you the `"+role.name+"` role")
						except:
							await bot.say("Error")
					elif role in ctx.message.author.roles:
						await bot.remove_roles(ctx.message.author, role)
						await bot.say("Successfully removed the `"+role.name+"` role from you")
				else:
					await bot.say("Sorry, I do not have permission to set roles.\nDisabling !role now")
					await bot_disable(ctx.message.server, 'role')
			else:
				await bot.say("That is not a valid role")
		else:
			await bot.say("Unable to find that role")
	else:
		await bot.say("Role setting is disabled")

#Function to disable bot commands serverside
async def bot_disable(server, command):
	with open('config.json', 'r') as j:
		config=json.load(j)
		await update_data(config, server)
	config[server.id]["enabled"][command]=0
	with open("config.json", "w") as j:
		json.dump(config, j, indent=4, sort_keys=True)

#Function to update json file
async def update_data(config, server):
	if not server.id in config:
		config[server.id]={}
		config[server.id]["enabled"]={}
		config[server.id]["enabled"]['join']=1
		config[server.id]["enabled"]['leave']=1
		config[server.id]["enabled"]['kick']=1
		config[server.id]["enabled"]['ban']=1
		config[server.id]["enabled"]['purge']=1
		config[server.id]["enabled"]['report']=0
		config[server.id]["enabled"]['invite']=0
		config[server.id]["enabled"]['swear']=1
		config[server.id]["enabled"]['role']=0
		config[server.id]["enabled"]['joinDm']=0
		config[server.id]["joinleaveChannel"]=""
		config[server.id]["reportChannel"]=""
		config[server.id]["joinDmText"]=""
		config[server.id]["joinMsgText"]=""
		config[server.id]["leaveMsgText"]=""
		config[server.id]["role"]=[]


#Function to make it easier for commands to check their config
async def check_config(command, server, outsideEnabled):
	try:
		with open('config.json', 'r') as j:
			config=json.load(j)
		await update_data(config, server)
		if (outsideEnabled==False):
			return config[server.id]["enabled"][command]
		else:
			return config[server.id][command]
	except:
		return

#Opens words file
if (os.path.exists('words')==False):
	os.mkdir('words')
i=1
while (i<=3):
	if (os.path.exists('words/words'+str(i)+'.txt')==False):
		open('words/words'+str(i)+'.txt', "w")
	i+=1
if (os.path.exists('config.json')==False):
	open('config.json', "w")
	
if (os.path.exists('key.config')==False):
	open('key.config', "w")
words1=open('words/words1.txt', 'r').read().lower().splitlines()
words2=open('words/words2.txt', 'r').read().lower().splitlines()
words3=open('words/words3.txt', 'r').read().lower().splitlines()

#Bot Token
bot.run(open('key.config', 'r').read())