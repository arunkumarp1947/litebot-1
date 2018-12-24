# litebot
Litebot is a dicord bot for simple moderation. It can delete messages containing banned words, announce when users join or leave the server, report a user to the owner and more. More features are coming soon

## To do
- ☑ Deletes messages containing any words in words.txt
- ☑ Join & Leave messages
- ☑ Kicking & Banning commands
- ☑ Report function
- ☑ Purge Messages 
- ☑ Help command
- ☑ Invite blocking
- ☑ Server specific disabling/enabling commands
- ☑ Better config - Set channel for join/leave messages
- ☑ Better Report System (Set which channel or user the reports go to)
- ☑ Better Swear blocking system (Different levels of swear blocking)
- ☐ Add verification system for channels (Check on !set to see if the channel works)
- ☐ Add support for minimal permissions
- ☐ New prefix
- ☐ Roles from reaction

## Most Likely not going to do
- ☐ Music System
- ☐ Purge specific user's messages
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
- Use `!set report #reports` to set the report channel to either a channel or a user
- Use `!report @username#0000 "Sample report content"` to report
- Report content must be in quotation marks if the report content is multiple words
### Purge
- Deletes the specified number of messages
- User must have delete message perm or admin perm
- Use `!purge 20`
### Enable/Disable
- Used to enable or disable a command
- Use `!enable <command>` or `!disable <command>`
### Set
- Sets a command to a specified value
- Use `!set <command> <value>`
