# LuigiBot (o!)
## A bot to replicate /r/askouija on Discord
This bot replicates /r/askouija where people can only respond with one letter at a time and must create a phrase to respond to the question/statment said.
- To ask a question use o!ask (question). If you want a fill in the blanks part in your question add '{}' where you want the blank.
- To help respond to a question say any character or 'space'
- To end the question you type 'goodbye' or 'Goodbye' and it will mention the user that asked the question saying the answer in an embed
## To work the channel must be named:
- ask-ouija
- askouija
- ouija
- ouijaboard
- ask-luigi
- askluigi
- luigiboard
## Luigi must have permissions (in that channel) to:
- Read Meassges
- Read Message History
- Send Messages
## Optionally Luigi can have permissions to:
- Add Reactions (in that channel)
  - To react to the accepted messages with ✅
- Manage Messages (in that channel)
  - To delete messages that don't fit the format (1 letter, space or goodbye)
  - To pin and unpin the message with the question
- Manage Roles
  - To give and take away the role mentioned in the next section.
### Role Pinging
There is also a feature to have a role that will get pinged when a new Question begins, to make this role it needs to be named 'Luigi' and luigibot must have to ability to give roles and be above the Luigi role.

> Made by JdavisBro

### Mood command
Mood command made by lit af guy [01-Grimm](https://github.com/01-Grimm/) from his [fork](https://github.com/01-Grimm/luigibot). Does a sentimental analysis on your last 15 out of 200 messages in a channel and tells you the % of happy you are.

[Me Hosting Bot Invite](https://discordapp.com/api/oauth2/authorize?client_id=557320040127397888&scope=bot&permissions=0)

## Self Hosting

If you would like to host the bot yourself, clone the thing and run luigi.py either through the start.sh file already there (which you need to edit to add your bot token) or by running `python3 luigi.py 'BOTTOKEN'` or `python3 luigi.py BOTTOKEN` (sometimes with ' it doesn't work idk why lol)
