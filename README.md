# litebot

## NOTE: Discord.py 1.0.0 has made some major changes that litebot is not compatible with. However, it still currently runs on version 0.16.12 with no major issues

Litebot is a discord bot for simple moderation with the prefix `+`. It can delete messages containing banned words, announce when users join or leave the server, report a user to the owner and more.
## Invite

[Invite Litebot Here](https://discordapp.com/oauth2/authorize?client_id=405829095054770187&scope=bot&permissions=11278)

## Features
- Join/Leave messages 
- Dm users on joining
- Kick or ban users
- Purge messages
- Report users to server moderators
- Block messages containing server invites, links and/or swearing
- Set roles from command

## To do
- ☐ Auto-Ban users after set number of warnings
- ☐ Logging channel

# Docs

### Join Message
- Sends a message when a user joins the Server
- "Welcome @username#0000"
- Can be enabled/disabled with `!enable join`
### JoinDm Message
- Sends a direct message when a user joins the Server
- Can be enabled/disabled with `!enable joindm`
- Can be set with `!config joindm <message>`
### Leave Message
- Sends a message when a user leaves the Server
- "**username** has left the server"
- Can be enabled/disabled with `!enable leave`
### Swear Blocking
- Deletes messages containing words depending on the level swear blocking is set to (Goes from 0-3)
- If the command is disabled, it is set to 0
- Can be enabled/disabled with `!enable swear`(If enabled it defaults to 1)
- Can be set with `!set swear 2`
### Invite Blocking
- Deletes messages contaning `discord.gg`
- Won't delete messages by admins
- Can be enabled/disabled with `!enable invite`
### Link Blocking
- Deletes messages contaning `http://` or 'https://'
- Won't delete messages by admins
- Can be enabled/disabled with `!enable link`
### Kick
- Kicks a user
- Kick via mention `!kick @username#0000`
- Can be enabled/disabled with `!enable kick`
### Ban
- Bans a user
- Ban via mention `!ban @username#0000`
- Can be enabled/disabled with `!enable ban`
### Report
- Sends a report to wherever the report channel is set to
- `!set report #reports` to set the report channel to either a channel or a user
- `!report @username#0000 Sample report content` to report
### Purge
- Deletes the specified number of messages
- User must have delete message perm or admin perm
- Can only purge between 0-100 messages
-`!purge 20`
### Enable/Disable  
- Used to enable or disable a command
- Use `!enable <command>` or `!disable <command>`
### Config
- Sets a command to a specified value
- Must have admin
- `!config <command> <value>`
### Check
- Checks what is enabled
- Displays which commands are enabled/disabled and what text is set to what
### setroles
- Sets roles that can be set by users
- roles are seperated by commas `,`
- Must have admin
- `!setroles <role1>,<role2>,<role3>
### Role
- Sets roles for users that usually can't change theirs
- Can be enabled/disabled
- `!role <role>`
