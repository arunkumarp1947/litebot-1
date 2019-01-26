# litebot
Litebot is a dicord bot for simple moderation. It can delete messages containing banned words, announce when users join or leave the server, report a user to the owner and more. More features are coming soon
## Invite

[Invite Litebot Here](https://discordapp.com/oauth2/authorize?client_id=405829095054770187&scope=bot&permissions=11278)

## To do
- ☑ Deletes messages containing any words in words (Different levels of swear blocking)
- ☑ Join & Leave messages
- ☑ Kicking & Banning commands
- ☑ Report command (Set which channel or user the reports go to)
- ☑ Purge Messages 
- ☑ Help command
- ☑ Invite blocking
- ☑ Server specific disabling/enabling commands & channels for join/leave
- ☑ Support for minimal permissions
- ☑ Check command to see what commands are enabled
- ☑ Roles from command
- ☑ Custom DM to new users
- ☑ Custom text for join/leave
- ☐ Rotating MOTD
- ☐ Log channel
- ☐ Clean up Code
- ☐ New/custom prefix

## Most Likely not going to do
- ☐ Music System
- ☐ Currency

# Docs

### Join Message
- Sends a message when a user joins the Server
- "Welcome @username#0000"
- Can be enabled/disable with `!enable join`
### Leave Message
- Sends a message when a user leaves the Server
- "**username** has left the server"
- Can be enabled/disable with `!enable leave`
### Swear Blocking
- Deletes messages containing words depending on the level swear blocking is set to (Goes from 0-3)
- If swear level is set to 2, it deletes messages contained in words1 & words2
- If the swear level is set to 3, it deletes messages contained in words1, words2 & words3
- If the command is disabled, it is set to 0
- Can be enabled/disable with `!enable swear`(If enabled it defaults to 1)
- Can be set with `!set swear 2`
### Invite Blocking
- Deletes messages contaning `discord.gg`
- Won't delete messages by admins
- Can be enabled/disable with `!enable invite`
### Kick
- Kicks a user
- Kick via mention `!kick @username#0000`
- Can be enabled/disable with `!enable kick`
### Ban
- Bans a user
- Ban via mention `!ban @username#0000`
- Can be enabled/disable with `!enable ban`
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
### Set
- Sets a command to a specified value
- Must have admin
- `!set <command> <value>`
### Check
- Checks what is enabled
### setroles
- Sets roles that can be set by users
- roles are seperated by commas `,`
- Must have admin
- `!setroles <role1>,<role2>,<role3>
### Role
- Sets roles for users that usually can't change theirs
- Can be enabled/disabled
- `!role <role>`
