import discord, logging, asyncio
from discord.ext import commands
import random, time, datetime
import json, sys
from textblob import TextBlob # Mood Command
import pytz
from pytz import timezone

logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s', level=logging.INFO)

try:
    open("prefixes.json","x")
    open("prefixes.json","w").write("{}")
    logging.info("prefixes.json created, used to store per server prefixes.")
except:
    logging.info("prefixes.json already exists or was unable to be created.")

try:
    open("timezones.json","x")
    open("timezones.json","w").write("{}")
    logging.info("timezones.json created, used to store timezones.")
except:
    logging.info("timezones.json already exists or was unable to be created.")

with open("prefixes.json","r") as f:
    prefixes = json.load(f)

default_prefix = "o!"

def prefix(bot, message):
    return str(prefixes.get(message.guild.id, default_prefix)) if message.guild != None else default_prefix

bot = commands.Bot(command_prefix=prefix,description="A bot to replicate /r/askouija on Discord!")
try:
    TOKEN = sys.argv[1]
except:
    logging.warning("Unable to get token, you must put it as the first argument after the file name, e.g python luigi.py 'TOKEN' or you can edit the code directly.")
    exit()
channel_names = ["ask-ouija","askouija","ouija","ouijaboard","ask-luigi","askluigi","luigiboard"]
bot.startTime = time.time()
update=0
on = {}
bot.question = {}
bot.answer = {}
bot.msg = {}
bot.messageembed = {}
bot.prevuser = {}
bot.origauthor = {}
bot.help_message = "Hello! I am LuigiBot (patent pending). I am a robot to replicate r/askouija on discord.\nTo be used I require a channel with one of the names as said on my github page's readme <https://www.github.com/jdavisbro/luigibot> permissions that I require or that are optional are also stated on that page. \nAfter that is sorted, asking a question is easy! Just go into the channel and type `{0}ask QUESTION` and I will wait for responses and add them.\nThe responses I look for are any one letter character (besides {{ and }}), 'space' for adding a space :| and goodbye for ending a question.\nOnce a question is ended I will pin the message to the channel, there is a limit to 50 pins though so I can't pin them all!\nThat you for coming to my TED talk. My prefix in this server is `{0}`"

@bot.event
async def on_ready():
    game = discord.Game(name='with my LuigiBoard. o!help')
    await bot.change_presence(status=discord.Status.online, activity=game)
    global appinfo, owner
    appinfo = await bot.application_info()
    owner = appinfo.owner
    logging.info('-'*(32 + len(str(bot.user))+len(str(bot.user.id))))
    logging.info('| Connected to DISCORD as {} -- {} |'.format(str(bot.user),bot.user.id))
    logging.info('-'*(32 + len(str(bot.user))+len(str(bot.user.id))))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        channel = ctx.channel
        if channel.name in channel_names:
            await ctx.send("Command not found, if you are trying to ask a question use o!ask")
        return
    raise error

def setquestion(channelid,question):
    bot.question[channelid] = question

def setanswer(channelid,answer):
    bot.answer[channelid] = answer

def setmsg(channelid,msg):
    bot.msg[channelid] = msg

def setembed(channelid,messageembed):
    bot.messageembed[channelid] = messageembed

def setprevuser(channelid,prevuser):
    bot.prevuser[channelid] = prevuser

def setuser(channelid,user):
    bot.origauthor[channelid] = user

@bot.event
async def on_message(message):
    global on, owner, channel_names
    if type(message.channel) is not discord.DMChannel:
        if message.guild.id not in on.keys():
            on[message.guild.id] = 0
        if on[message.guild.id] != 0:
            if message.channel.name in channel_names:
                if (message.author == owner or message.author == message.guild.me) and message.content.startswith("##"):
                    return
                if on[message.guild.id] == 1:
                    await message.delete()
                    return
                question = bot.question[message.guild.id]
                answer = bot.answer[message.guild.id]
                msg = bot.msg[message.guild.id]
                embed = bot.messageembed[message.guild.id]
                prevuser = bot.prevuser[message.guild.id]
                user = bot.origauthor[message.guild.id]
                length = len(message.content)
                if not message.author.bot:
                    if length == 1 and message.author != user and message.author != prevuser and message.content != '{':
                        answer = answer.replace('{}', message.content + '{}')
                        embed.add_field(name='The current answer is:', value='"{}"'.format(answer.replace('{}', '')), inline=False)
                        try:
                            await message.add_reaction('✅')
                        except:
                            pass
                        await msg.edit(embed=embed)
                        embed.clear_fields()
                        prevuser = message.author
                        setprevuser(message.guild.id,prevuser)
                        setanswer(message.guild.id,answer)
                        await asyncio.sleep(0.5)
                    elif message.content == 'space' or message.content == 'Space' and message.author != user and message.author != prevuser:
                        answer = answer.replace('{}', '␣{}')
                        embed.add_field(name='The current answer is:', value='"{}"'.format(answer.replace('{}', '')), inline=False)
                        try:
                            await message.add_reaction('✅')
                        except:
                            pass
                        await msg.edit(embed=embed)
                        embed.clear_fields()
                        prevuser = message.author
                        setprevuser(message.guild.id,prevuser)
                        setanswer(message.guild.id,answer)
                        await asyncio.sleep(0.5)
                    elif (message.content == 'goodbye' or message.content == 'Goodbye') and message.author != user and message.author != prevuser:
                        on[message.guild.id] = 0
                        setprevuser(message.guild.id,'')
                        if answer == '':
                            answer = ' '
                        answer=answer.replace("␣"," ")
                        embed = discord.Embed(title="We have the answer to {}'s question!".format(user.name), description='The question was "{}"'.format(question), color=2151680)
                        embed.set_author(name='Ouija Question!', url='https://discord.gg/UGsdqwk', icon_url='https://www.fjordsafari.com/wp-content/uploads/2016/11/question-mark-4-xxl.png')
                        embed.add_field(name='The answer is', value='"{}"'.format(answer).replace('{}', ''), inline=False)
                        msg1 = await message.channel.send("We have the answer to {}'s question!".format(user.mention))
                        pinme = await message.channel.send(embed=embed)
                        await msg.unpin()
                        await asyncio.sleep(0.5)
                        await msg1.delete()
                        await pinme.pin()
                        answer = ''
                        logging.info('OFF in {}'.format(message.guild.name))
                    elif message.content == 'stopouija' and message.author == owner:
                        on[message.guild.id] = 0
                        logging.info('{} used stopouija to stop the question going on in {}'.format(str(owner),message.guild.name))
                    else:
                        await bot.process_commands(message)
                        try:
                            await message.delete()
                        except:
                            pass
                else:
                    await bot.process_commands(message)
                    try:
                        await message.delete()
                    except:
                        pass
            elif message.content == "<@{}>".format(bot.user.id) or message.content == "<@!{}>".format(bot.user.id):
                await message.channel.send(bot.help_message.format(prefixes.get(message.guild.id,default_prefix)))
            else:
                if not message.author.bot:
                    if message.content.startswith("if you are real say "):
                        send=message.content.replace("if you are real say ","")
                        await message.channel.send("{}, lol".format(send))
                await bot.process_commands(message)
        elif not message.author.bot and message.content.startswith("if you are real say "):
            send=message.content.replace("if you are real say ","")
            await message.channel.send("{}, lol".format(send))
        elif message.content == "<@{}>".format(bot.user.id) or message.content == "<@!{}>".format(bot.user.id):
            await message.channel.send(bot.help_message.format(prefixes.get(message.guild.id,default_prefix)))
        else:
            await bot.process_commands(message)
    elif not message.author.bot and message.content.startswith("if you are real say "):
        send=message.content.replace("if you are real say ","")
        await message.channel.send("{}, lol".format(send))
    elif message.content == "<@{}>".format(bot.user.id) or message.content == "<@!{}>".format(bot.user.id):
        await message.channel.send(bot.help_message.format(prefixes.get(message.guild.id,default_prefix)))
    else:
        await bot.process_commands(message)

@bot.command()
async def ask(ctx,*,question):
    "Asks a question! Can only be used in a channel named 'ask-ouija'"
    global update
    if update == 0:
        if ctx.guild.id not in on.keys():
            on[ctx.guild.id] = 0
        if on[ctx.guild.id] == 0:
            user = ctx.author
            if ctx.channel.name in channel_names:
                on[ctx.guild.id] = 1
                logging.info("ON in {}".format(ctx.guild.name))
                answer = ''
                if '{}' in question:
                    answer = question
                else:
                    answer = '{}'
                setuser(ctx.guild.id,user)
                setquestion(ctx.guild.id,question)
                setanswer(ctx.guild.id,answer)
                setprevuser(ctx.guild.id,"")
                embed = discord.Embed(title="A question has come in! Say one letter or 'space' to answer it! ", description='"{}"'.format(question), color=6363163)
                embed.set_author(name='Ouija Question!', icon_url='https://www.fjordsafari.com/wp-content/uploads/2016/11/question-mark-4-xxl.png')
                embed.add_field(name='The current answer is:', value='"{}"'.format(answer.replace('{}', ' ')), inline=False)
                embed.set_footer(text='Question by {} ({})'.format(user.display_name,user))
                try:
                    role=discord.utils.get(ctx.guild.roles, name='Luigi')
                    msg = await ctx.send(content='## {}: {} (in {}) has asked "{}"!'.format(role.mention,user.name,ctx.guild.name,question),embed=embed)
                except:
                    msg = await ctx.send(content="##",embed=embed)
                    pass
                await msg.edit(content="",embed=embed)
                try:
                    await msg.pin()
                except:
                    pass
                await asyncio.sleep(0.5)
                embed.clear_fields()
                setmsg(ctx.guild.id,msg)
                setembed(ctx.guild.id,embed)
                on[ctx.guild.id] = ctx.channel.id
            else:
                await asyncio.sleep(0.5)
        else:
            await asyncio.sleep(0.5)
            try:
                await ctx.message.delete()
            except:
                pass
            await ctx.send("## There is already a question going on in this server.",delete_after=5)
    else:
        await ctx.send("Ouija is not allowed to start as there is an update soon!")

@bot.command()
@commands.is_owner()
async def exit(ctx):
    'Stops the bot, only usable by the owner.'
    await ctx.send('Goodbye! 👋')
    await bot.close()

@bot.command()
async def setprefix(ctx,prefixToBeSet="o!"):
    'Sets the command prefix for this server, only usable by a user that has the Manage Server permissions, if the prefix you want contains space put it in "quotes". Defaults to `o!` if no prefix is specified'
    if ctx.author.guild_permissions.manage_guild or ctx.author == ctx.guild.owner:
        prefixes[ctx.guild.id] = prefixToBeSet
        await ctx.send("Prefix for {} set to `{}`".format(ctx.guild.name,prefixToBeSet))
        with open("prefixes.json","w") as f:
            f.write(str(json.dumps(prefixes)))
            f.flush()

@bot.command()
async def uptime(ctx):
    'Shows you how long the bot has been online'
    currentTime = time.time()
    uptime = int(round(currentTime - bot.startTime))
    uptime = str(datetime.timedelta(seconds=uptime))
    colour = discord.Colour.from_rgb(random.randint(1,255),random.randint(1,255),random.randint(1,255))
    embed = discord.Embed(title="I have been up for", description=uptime, color=colour)
    await ctx.send(embed=embed)

@bot.command()
async def role(ctx):
    'Gives you the Luigi role if it exists in the server, the role gets pinged whenever a new Ouija starts!'
    member = ctx.author
    try:
        role = discord.utils.get(ctx.guild.roles, name='Luigi')
    except:
        await ctx.send("This server doesn't have a Luigi role.")
        return
    await ctx.send('Ok, {} has been given the Luigi role!'.format(ctx.author.name))
    await member.add_roles(role)

@bot.command()
async def unrole(ctx):
    'Removes the Luigi role if you have it (and if it exists in the server)!'
    member = ctx.author
    try:
        role = discord.utils.get(ctx.guild.roles, name='Luigi')
    except:
        await ctx.send("This server doesn't have a Luigi role.")
        return
    await ctx.send('Ok, {} has been removed from the Luigi role!'.format(ctx.author.name))
    member = ctx.author
    await member.remove_roles(role)


@bot.group(aliases=['send'])
@commands.is_owner()
async def say(ctx):
    'Makes the bot say something, only usable by the owner'
    if ctx.invoked_subcommand is None:
        await ctx.send_help(ctx.command)
    

@say.command(name='here',aliases=['h'])
async def say_here(ctx,*,say):
    'Makes say in the channel you use this in lol'
    try:
        await ctx.message.delete()
    except:
        pass
    await ctx.channel.trigger_typing()
    await asyncio.sleep(0.4)
    await ctx.send(say.format(ctx))

@say.command(name='channel')
async def say_channel(ctx,channel: discord.TextChannel,*,say):
    'Makes say in a channel lol'
    try:
        await ctx.message.delete()
    except:
        pass
    await channel.trigger_typing()
    await asyncio.sleep(0.4)
    await channel.send(say.format(ctx))

@bot.command()
@commands.is_owner()
async def updatesoon(ctx):
    'Stops new Questions from being asks and shuts down ongoing ouijas after 5 minutes, only usable by the owner'
    ouijasactive = 0
    global on, update
    update = 1
    for channelid in on.values():
        if channelid != 0:
            ouijasactive += 1
            channel = bot.get_channel(channelid)
            try:
                role=discord.utils.get(channel.guild.roles, name='Luigi')
                await channel.send("## {}! This Ouija will be shut down in 5 minutes as there will be an update soon.".format(role.mention))
            except:
                await channel.send("## This Ouija will be shut down in 5 minutes as there will be an update soon.")
    if ouijasactive == 0:
        await ctx.send("Looks like there are no Ouija instances running!")
        return
    else:
        await ctx.send("Closing Down {} Questions in 5 Minutes".format(str(ouijasactive)))
    await asyncio.sleep(300)
    for channelid in on.values():
        if channelid != 0:
            channel = bot.get_channel(channelid)
            await channel.send("Shutting Down Ouija.")
            question = bot.question[channel.guild.id]
            answer = bot.answer[channel.guild.id]
            msg = bot.msg[channel.guild.id]
            embed = bot.messageembed[channel.guild.id]
            user = bot.origauthor[channel.guild.id]
            on[channel.guild.id] = 0
            setprevuser(channel.guild.id,'')
            if answer == '':
                answer = ' '
            embed = discord.Embed(title="We have the answer to {}'s question!".format(user.name), description='The question was "{}"'.format(question), color=2151680)
            embed.set_author(name='Ouija Question!', url='https://discord.gg/UGsdqwk', icon_url='https://www.fjordsafari.com/wp-content/uploads/2016/11/question-mark-4-xxl.png')
            embed.add_field(name='The answer is', value='"{}"'.format(answer).replace('{}', ''), inline=False)
            msg1 = await channel.send("We have the answer to {}'s question!".format(user.mention))
            pinme = await channel.send(embed=embed)
            await msg.unpin()
            await asyncio.sleep(0.5)
            await msg1.delete()
            await pinme.pin()
            answer = ''
            logging.info('FORCED OFF in {}'.format(channel.guild.name))
    await ctx.send("{}! Ouija instances shut down!".format(ctx.author.mention))

@bot.command()
@commands.is_owner()
@commands.dm_only()
async def servers(ctx):
    'Lists the servers the bot is in, only usable by the owner in DMs'
    guilds = ''
    for guild in bot.guilds:
        guilds += guild.name + '\n'
    await ctx.send(guilds)

@bot.command()
async def mood(ctx,user: discord.Member=None, channel: discord.TextChannel=None):
    'Finds out how a user is doing using sentiment analysis'
    if not user:
        user = ctx.author
    if not channel:
        channel = ctx.channel
    async with ctx.channel.typing():
        counter = 0             # Getting user's last 15 messages
        serverprefix = prefix(bot,ctx.message)
        user_messages = []
        async for message in channel.history(limit=200):
            if (not message.content.startswith(serverprefix)) and message.author == user:  # making sure not to analyze "o!mood" message as well as only adding messages from user
                user_messages.append(message.content)
                counter += 1
            if counter > 15:
                break
        if counter == 0:
            await ctx.send("You have send 0 messages (not beginning with '{}') within the last 200 messages in this channel.".format(serverprefix))
            return
        sentiments = []
        for message in user_messages:
            opinion = TextBlob(message).sentiment # Getting opinion of message
            sentiments.append((opinion.polarity + 1) / 2) # Adding message's sentiment to sentiment array (opinion.sentiment.polarity is -1.0 - 1.0, so it is normalized)
        overall_sentiment = sum(sentiments) / len(sentiments) # Averaging out sentiments
    await ctx.send("{} is {}% happy!".format(user.display_name, int(overall_sentiment * 100))) # overall_sentiment is converted to an percentage without a fractional
    
@bot.group(name="timezone",aliases=["tz"])
async def tz(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send_help(ctx.command)

@tz.command(name="add")
async def tz_add(ctx,timezonee: str):
    f = open("timezones.json","r")
    timezones = json.loads(f.read())
    try:
        timezones[str(ctx.guild.id)]
    except KeyError:
        timezones[str(ctx.guild.id)] = []
    timezonee = timezonee.upper()
    if timezonee in timezones[str(ctx.guild.id)]:
        await ctx.send("That timezone is already in the list.")
        return
    if timezonee not in list(pytz.all_timezones):
        await ctx.send("That is not a timezone")
        return
    await ctx.send(f"Timezone {timezonee} added to the list.")
    timezones[str(ctx.guild.id)].append(timezonee)
    open("timezones.json","w").write(json.dumps(timezones))

@tz.command(name="del",aliases=["remove","delete"])
async def tz_del(ctx,timezonee: str):
    f = open("timezones.json","r")
    timezones = json.loads(f.read())
    try:
        timezones[str(ctx.guild.id)]
    except KeyError:
        timezones[str(ctx.guild.id)] = []
    timezonee = timezonee.upper()
    if timezonee not in timezones[str(ctx.guild.id)]:
        await ctx.send("That timezone isn't in the list.")
        return
    await ctx.send(f"Timezone {timezonee} removed from the list.")
    timezonee[str(ctx.guild.id)].pop(timezonee)
    open("timezones.json","w").write(json.dumps(timezones))

@tz.command(name="list")
async def tz_list(ctx):
    f = open("timezones.json","r")
    timezones = json.loads(f.read())
    try:
        timezones[str(ctx.guild.id)]
    except KeyError:
        timezones[str(ctx.guild.id)] = []
    if not timezones[str(ctx.guild.id)]:
        await ctx.send("There are no timezones for this server.")
        return
    message = "Here's the list of timezones for this server:\n"
    for timezoneee in timezones[str(ctx.guild.id)]:
        message += f"{timezoneee}\n"
    await ctx.send(message)

@tz.command(name="convert")
async def tz_convert(ctx,time:str,timezonee:str):
    timezonee = timezonee.upper()
    if timezonee not in list(pytz.all_timezones):
        await ctx.send("That is not a timezone")
        return
    time = datetime.datetime.strptime(time, '%H:%M').time()
    timezonee = timezone(timezonee)
    time = time.replace(tzinfo=timezonee)
    f = open("timezones.json","r")
    timezones = json.loads(f.read())
    try:
        timezones[str(ctx.guild.id)]
    except KeyError:
        timezones[str(ctx.guild.id)] = []
    if not timezones[str(ctx.guild.id)]:
        await ctx.send("There are no timezones in this server.")
        return
    message = "Here's that time in the timezones added to this server.\n"
    for timezoneee in timezones[str(ctx.guild.id)]:
        message += f"{timezoneee}: {time.astimezone(timezone(timezoneee))}\n"
    await ctx.send(message)
    
bot.run(TOKEN)
