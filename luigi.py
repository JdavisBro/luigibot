import discord, logging, asyncio # Normal Discord.py stuff
from discord.ext import commands # Normal Discord.py stuff
import random, time, datetime, json, sys # Uptime, Prefixes, Token
from textblob import TextBlob # Mood Command
import pytz # Timezone command
from pytz import timezone # Timezone command
import requests, shutil # Inspire me command
from variables import * # Get variables from variables.py

logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s', level=logging.INFO)

def jsonCheck(filename):
    try:
        open(f"{filename}.json","x")
        open(f"{filename}.json","w").write("{}")
        logging.info("{filename}.json created.")
    except:
        logging.info(f"{filename}.json already exists or was unable to be created.")

jsonCheck('prefixes')
jsonCheck('timezones')
#jsonCheck('embeds')

if TOKEN is None:
    try: # TOKEN
        TOKEN = sys.argv[1]
    except:
        logging.warning("Unable to get token, you must put it as the first argument after the file name, e.g python luigi.py 'TOKEN' or you can edit the code directly.")
        exit()
with open("prefixes.json","r") as f:
    prefixes = json.load(f)

def prefix(bot, message):
    return str(prefixes.get(str(message.guild.id), default_prefix)) if message.guild != None else default_prefix

game = discord.Game('Starting Up ⬆')
bot = commands.Bot(command_prefix=prefix,description=description,activity=game)
bot.channel_names = channel_names
channel_names = None
bot.update = 0
on = {}
bot.question = {}
bot.answer = {}
bot.msg = {}
bot.embed = {}
bot.prevuser = {}
bot.origauthor = {}
bot.help_message = help_message
help_message = None

try:
    debug = True if sys.argv[2] == 'debug' or debug == True else False
    if debug:
        logging.warning("Debug mode is on, errors will stop commands but have more detail.")
except:
    debug = False

def setBot(variable,value,guildid=None):
    if guildid != None:
        exec(f"bot.{variable}[{guildid}] = value")
    else:
        exec(f"bot.{variable} = value")

@bot.event
async def on_ready():
    appinfo = await bot.application_info()
    setBot("appinfo",appinfo)
    setBot("startTime",time.time())
    logging.info('-'*(32 + len(str(bot.user))+len(str(bot.user.id))))
    logging.info('| Connected to DISCORD as {} -- {} |'.format(str(bot.user),bot.user.id))
    logging.info('-'*(32 + len(str(bot.user))+len(str(bot.user.id))))
    await asyncio.sleep(0.3)
    game = discord.Game('Started ✅')
    await bot.change_presence(activity=game)
    await asyncio.sleep(1.7)
    game = discord.Game(name=game_name.format(str(bot.user)))
    await bot.change_presence(status=discord.Status.online, activity=game)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        channel = ctx.channel
        server_prefix = ''
        server_prefix = prefix(bot,ctx)
        if channel.name in bot.channel_names:
            await ctx.send(f"Command not found, if you are trying to ask a question use {server_prefix}ask")
        return
    if not debug:
        logging.warning(error)
    else:
        raise error

async def addResponce(message,content=None):
    if content is None:
        content = message.content
    answer = bot.answer[message.guild.id]
    msg = bot.msg[message.guild.id]
    embed = bot.embed[message.guild.id]
    answer = answer.replace('{}', content + '{}')
    embed.add_field(name="The current answer is", value="'{}'".format(answer.replace("{}","")))
    try:
        await message.add_reaction('✅')
    except:
        pass
    await msg.edit(embed=embed)
    embed.clear_fields()
    setBot("prevuser",message.author,message.guild.id)
    setBot("answer",answer,message.guild.id)

async def messageExtras(message):
    if message.author.bot:
        return
    if message.content.lower().startswith("inspire me"):
        await message.channel.trigger_typing()
        image_url = requests.get('http://inspirobot.me/api?generate=true').text
        embed = discord.Embed(colour=discord.Colour.from_rgb(random.randint(1,255),random.randint(1,255),random.randint(1,255))).set_image(url=image_url)
        await message.channel.send(embed=embed)
        return
    if message.content.lower().startswith("if you are real say "):
        send=message.content.lower().replace("if you are real say ","")
        await message.channel.send("{}, lol".format(send))
        return
    if message.content == "<@{}>".format(bot.user.id) or message.content == "<@!{}>".format(bot.user.id):
        server_prefix = prefix(bot,message)
        await message.channel.send(bot.help_message.format(server_prefix))
        return
    await bot.process_commands(message)

@bot.event
async def on_message(message):
    didSomething = 0
    if type(message.channel) is not discord.DMChannel:
        if message.guild.id not in on.keys():
            on[message.guild.id] = 0
        if on[message.guild.id] != 0 and message.channel.name in bot.channel_names:
            if (message.author == bot.appinfo.owner or message.author == message.guild.me) and message.content.startswith("##"):
                return
            if on[message.guild.id] == 1:
                try:
                    await message.delete()
                except:
                    pass
                return
            on[message.guild.id] == 1
            didSomething = 1
            prevuser = bot.prevuser[message.guild.id]
            user = bot.origauthor[message.guild.id]
            length = len(message.content)
            if not message.author.bot:
                if length == 1 and message.author != user and message.author != prevuser and message.content != '{':
                    await addResponce(message)
                    didSomething = 2
                elif message.content.lower() == 'space' and message.author != user and message.author != prevuser:
                    await addResponce(message,'␣')
                    didSomething = 2
                elif (message.content == f"<:{message.content.replace('<:','').replace('>','')}>" or message.content == f"<a:{message.content.replace('<a:','').replace('>','')}>") and message.author != user and message.author != prevuser:
                    emoji_id = int(message.content[message.content.find(':',3)+1:].replace('>',''))
                    emoji = bot.get_emoji(emoji_id)
                    if emoji is not None:
                        await addResponce(message,str(emoji))
                        didSomething = 2
                elif message.content.lower() == 'goodbye' and message.author != user and message.author != prevuser:
                    question = bot.question[message.guild.id]
                    answer = bot.answer[message.guild.id]
                    msg = bot.msg[message.guild.id]
                    embed = bot.embed[message.guild.id]
                    on[message.guild.id] = 0
                    setBot("prevuser",'',message.guild.id)
                    if answer == '':
                        answer = ' '
                    answer=answer.replace("␣"," ")
                    embed = discord.Embed(title="We have the answer to {}'s question!".format(user.name), description='The question was: {}'.format(question), color=2151680)
                    embed.set_author(name='Ouija Question!',icon_url='https://d30y9cdsu7xlg0.cloudfront.net/png/57788-200.png')
                    embed.add_field(name="The answer is", value="'{}'".format(answer.replace("{}","")))
                    msg1 = await message.channel.send("We have the answer to {}'s question!".format(user.mention))
                    pinme = await message.channel.send(embed=embed)
                    await msg.unpin()
                    await asyncio.sleep(0.5)
                    await msg1.delete()
                    await pinme.pin()
                    answer = ''
                    logging.info('OFF in {}'.format(message.guild.name))
                    didSomething = 2
                elif message.content == 'stopouija' and message.author == bot.appinfo.owner:
                    on[message.guild.id] = 0
                    logging.info('{} used stopouija to stop the question going on in {}'.format(str(bot.appinfo.owner),message.guild.name))
                    didSomething = 2
    if didSomething == 0:
        await messageExtras(message)
    else:
        if didSomething == 1:
            await message.delete()
        on[message.guild.id] = (message.channel.id if on[message.guild.id] != 0 else 0)

class Ouija(commands.Cog):
    def __init__(self,bot): 
        self.bot = bot

    @commands.command()
    async def ask(self,ctx,*,question):
        "Asks a question! Can only be used in a channel named 'ask-ouija'"
        if self.bot.update == 0:
            if ctx.guild.id not in on.keys():
                on[ctx.guild.id] = 0
            if on[ctx.guild.id] == 0:
                user = ctx.author
                if ctx.channel.name in self.bot.channel_names:
                    on[ctx.guild.id] = 1
                    logging.info("ON in {}".format(ctx.guild.name))
                    answer = ''
                    if '{}' in question:
                        answer = question
                    else:
                        answer = '{}'
                    setBot('origauthor',user,ctx.guild.id)
                    setBot('question',question,ctx.guild.id)
                    setBot('answer',answer,ctx.guild.id)
                    setBot('prevuser','',ctx.guild.id)
                    embed = discord.Embed(title="A question has come in! Say one letter or 'space' to answer it! ", description=question, color=6363163)
                    embed.set_author(name='Ouija Question!', icon_url='https://d30y9cdsu7xlg0.cloudfront.net/png/57788-200.png')
                    embed.add_field(name="The current answer is", value="'{}'".format(answer.replace("{}"," ")))
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
                    setBot('msg',msg,ctx.guild.id)
                    setBot('embed',embed,ctx.guild.id)
                    on[ctx.guild.id] = ctx.channel.id
            else:
                await asyncio.sleep(0.5)
                try:
                    await ctx.message.delete()
                except:
                    pass
                await ctx.send("## There is already a question going on in this server.",delete_after=5)
        else:
            await ctx.send("Ouija is not allowed to start as there is an update soon!")

    @commands.command()
    async def role(self,ctx):
        'Gives you the Luigi role if it exists in the server, the role gets pinged whenever a new Ouija starts!'
        member = ctx.author
        try:
            role = discord.utils.get(ctx.guild.roles, name='Luigi')
        except:
            await ctx.send("This server doesn't have a Luigi role.")
            return
        await ctx.send('Ok, {} has been given the Luigi role!'.format(ctx.author.name))
        await member.add_roles(role)

    @commands.command()
    async def unrole(self,ctx):
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

class Owner(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def exit(self,ctx):
        'Stops the bot, only usable by the owner.'
        await ctx.send('Goodbye! 👋')
        await self.bot.close()

    @commands.group(aliases=['send'])
    @commands.is_owner()
    async def say(self,ctx):
        'Makes the bot say something, only usable by the owner'
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)
        

    @say.command(name='here',aliases=['h'])
    async def say_here(self,ctx,*,say):
        'Makes say in the channel you use this in lol'
        try:
            await ctx.message.delete()
        except:
            pass
        await ctx.channel.trigger_typing()
        await asyncio.sleep(0.4)
        await ctx.send(say.format(ctx))

    @say.command(name='channel')
    async def say_channel(self,ctx,channel: discord.TextChannel,*,say):
        'Makes say in a channel lol'
        try:
            await ctx.message.delete()
        except:
            pass
        await channel.trigger_typing()
        await asyncio.sleep(0.4)
        await channel.send(say.format(ctx))

    @commands.command()
    @commands.is_owner()
    async def updatesoon(self,ctx):
        'Stops new Questions from being asks and shuts down ongoing ouijas after 5 minutes, only usable by the owner'
        ouijasactive = 0
        setBot('update',1)
        for channelid in on.values():
            if channelid != 0:
                ouijasactive += 1
                channel = self.bot.get_channel(channelid)
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
                channel = self.bot.get_channel(channelid)
                await channel.send("Shutting Down Ouija.")
                question = self.bot.question[channel.guild.id]
                answer = self.bot.answer[channel.guild.id]
                msg = self.bot.msg[channel.guild.id]
                embed = self.bot.embed[channel.guild.id]
                user = self.bot.origauthor[channel.guild.id]
                on[channel.guild.id] = 0
                if answer == '':
                    answer = ' '
                embed = discord.Embed(title="We have the answer to {}'s question!".format(user.name), description='The question was: {}'.format(question), color=2151680)
                embed.set_author(name='Ouija Question!', icon_url='https://d30y9cdsu7xlg0.cloudfront.net/png/57788-200.png')
                embed.add_field(name="The current answer is", value="'{}'".format(answer.replace("{}","")))
                msg1 = await channel.send("We have the answer to {}'s question!".format(user.mention))
                pinme = await channel.send(embed=embed)
                try:
                    await msg.unpin()
                except:
                    pass
                await asyncio.sleep(0.5)
                await msg1.delete()
                try:
                    await pinme.pin()
                except:
                    pass
                logging.info('FORCED OFF in {}'.format(channel.guild.name))
        await ctx.send("{}! Ouija instances shut down!".format(ctx.author.mention))

    @commands.command()
    @commands.is_owner()
    async def servers(self,ctx):
        'Lists the servers the bot is in, only usable by the owner'
        guilds = '\n'.join([guild.name for guild in bot.guilds])
        await ctx.send(guilds)

class Mod(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def setprefix(self,ctx,prefixToBeSet="o!"):
        'Sets the command prefix for this server, only usable by a user that has the Manage Server permissions\nIf the prefix you want contains space put it in "quotes". Defaults to `o!` if no prefix is specified'
        prefixes[str(ctx.guild.id)] = prefixToBeSet
        await ctx.send("Prefix for {} set to `{}`".format(ctx.guild.name,prefixToBeSet))
        with open("prefixes.json","w") as f:
            f.write(str(json.dumps(prefixes)))
            f.flush()
    
    @commands.command(aliases=['cP','removePins'])
    @commands.has_permissions(manage_messages=True)
    async def clearPins(self,ctx,channel=None):
        async with ctx.channel.typing():
            if not channel:
                channel = ctx.channel
            pins = await channel.pins()
            if not pins:
                await ctx.send("There are no pins in this channel")
                return
            for pin in pins:
                await pin.unpin()
            await ctx.send("Done! ⛔📌")

class Other(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def uptime(self,ctx):
        'Shows you how long the bot has been online'
        currentTime = time.time()
        uptime = int(round(currentTime - self.bot.startTime))
        uptime = str(datetime.timedelta(seconds=uptime))
        colour = discord.Colour.from_rgb(random.randint(1,255),random.randint(1,255),random.randint(1,255))
        embed = discord.Embed(title="I have been up for", description=uptime, color=colour)
        await ctx.send(embed=embed)

    @commands.command()
    async def mood(self,ctx,user: discord.Member=None, channel: discord.TextChannel=None):
        'Finds out how a user is doing using sentiment analysis'
        if not user:
            user = ctx.author
        if not channel:
            channel = ctx.channel
        async with ctx.channel.typing():
            counter = 0             # Getting user's last 15 messages
            serverprefix = prefix(self.bot,ctx.message)
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
        
    @commands.group(name="timezone",aliases=["tz"])
    async def tz(self,ctx):
        """Converts times. Compatable timezones: https://jdavisbro.github.io/luigi/timezones.txt"""
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @tz.command(name="add")
    async def tz_add(self,ctx,timezonee: str):
        """Adds a timezone to the server list. Compatable timezones: https://jdavisbro.github.io/luigi/timezones.txt"""
        f = open("timezones.json","r")
        timezones = json.loads(f.read())
        try:
            timezones[str(ctx.guild.id)]
        except KeyError:
            timezones[str(ctx.guild.id)] = []
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
    async def tz_del(self,ctx,timezonee: str):
        """Removes timezones from the server list"""
        f = open("timezones.json","r")
        timezones = json.loads(f.read())
        try:
            timezones[str(ctx.guild.id)]
        except KeyError:
            timezones[str(ctx.guild.id)] = []
        if timezonee not in timezones[str(ctx.guild.id)]:
            await ctx.send("That timezone isn't in the list.")
            return
        await ctx.send(f"Timezone {timezonee} removed from the list.")
        timezones[str(ctx.guild.id)].remove(timezonee)
        open("timezones.json","w").write(json.dumps(timezones))

    @tz.command(name="list")
    async def tz_list(self,ctx):
        """Lists the timezones added to the server using tz add"""
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
    async def tz_convert(self,ctx,hour:int,minutes:int,timezonee:str):
        """Converts the given HOUR and MINUTE from TIMEZONEE to
        the timezones added to the server using tz add
        Compatable timezones: https://jdavisbro.github.io/luigi/timezones.txt"""
        if timezonee not in list(pytz.all_timezones):
            await ctx.send("That is not a timezone")
            return
        time = datetime.datetime.now()
        timezonee = timezone(timezonee)
        time = time.replace(tzinfo=timezonee,hour=hour,minute=minutes,second=0,microsecond=0)
        f = open("timezones.json","r")
        timezones = json.loads(f.read())
        try:
            timezones[str(ctx.guild.id)]
        except KeyError:
            timezones[str(ctx.guild.id)] = []
        if not timezones[str(ctx.guild.id)]:
            await ctx.send("There are no timezones in this server.")
            return
        embed = discord.Embed(title="Heres that time in the timezones added to the server.", colour=discord.Colour.from_rgb(random.randint(1,250),random.randint(1,250),random.randint(1,250)))
        for timezoneee in timezones[str(ctx.guild.id)]:
            timeinthistimezone = time.astimezone(timezone(timezoneee))
            if int(timeinthistimezone.strftime("%H")) > 12:
                timeinthistimezone = f"{timeinthistimezone.strftime('%H:%M')} ({int(timeinthistimezone.strftime('%H'))-12}:{timeinthistimezone.strftime('%M')}pm)"
            else:
                timeinthistimezone = f"{timeinthistimezone.strftime('%H:%M')} ({timeinthistimezone.strftime('%H:%M')}am)"
            embed.add_field(name=timezoneee, value=timeinthistimezone, inline=True)
        await ctx.send(embed=embed)

    @tz.command(name="currenttime",aliases=["current","now"])
    async def tz_current(self,ctx):
        """Converts the given HOUR and MINUTE from TIMEZONEE to
        the timezones added to the server using tz add
        Compatable timezones: https://jdavisbro.github.io/luigi/timezones.txt"""
        time = datetime.datetime.utcnow()
        f = open("timezones.json","r")
        timezones = json.loads(f.read())
        try:
            timezones[str(ctx.guild.id)]
        except KeyError:
            timezones[str(ctx.guild.id)] = []
        if not timezones[str(ctx.guild.id)]:
            await ctx.send("There are no timezones in this server.")
            return
        embed = discord.Embed(title="Heres the current time in the timezones added to the server.", colour=discord.Colour.from_rgb(random.randint(1,250),random.randint(1,250),random.randint(1,250)))
        for timezoneee in timezones[str(ctx.guild.id)]:
            timeinthistimezone = pytz.utc.localize(time).astimezone(timezone(timezoneee))
            if int(timeinthistimezone.strftime("%H")) > 12:
                timeinthistimezone = f"{timeinthistimezone.strftime('%H:%M')} ({int(timeinthistimezone.strftime('%H'))-12}:{timeinthistimezone.strftime('%M')}pm)"
            else:
                timeinthistimezone = f"{timeinthistimezone.strftime('%H:%M')} ({timeinthistimezone.strftime('%H:%M')}am)"
            embed.add_field(name=timezoneee, value=timeinthistimezone, inline=True)
        await ctx.send(embed=embed)

        @commands.command()
        async def reactors(self,ctx,emoji,messageid:int,channel:discord.TextChannel=None,randomise:int=None):
            channel = ctx.channel if channel is None else channel
            messages = await channel.history().flatten()
            message = discord.utils.get(messages,id=messageid)
            for reaction in message.reactions:
                if str(reaction.emoji) == emoji:
                    users = await reaction.users().flatten()
                    users = [str(user) for user in users]
                    msg = await ctx.send('\n'.join(users))
                    if randomise is not None:
                        for i in range(randomise):
                            await asyncio.sleep(1)
                            random.shuffle(users)
                            await msg.edit(content="{}\n{}/{}".format('\n'.join(users),i+1,randomise))
                    return
            await ctx.send("That emoji wasn't found on that message")

#class Embed(commands.Cog):
#    def __init__(self,bot):
#        self.bot = bot
#
#    @commands.group(name='embed')
#    async def embed_command(self,ctx):
#        if ctx.invoked_subcommand is None:
#            await ctx.send_help(ctx.command)
#        
#    @embed_command.command(name='add',aliases=['create','new'])
#    async def embed_command_add(self,ctx,*,title=None):
#        if title is None:
#            embed = discord.Embed()
#        else:
#            embed = discord.Embed(title=title)
#        f = open('embeds.json','r+')
#        embeds = json.load(f)
#        try:
#            guildembeds = json.loads(embeds[str(ctx.guild.id)])
#        except:
#            embeds[str(ctx.guild.id)] = {}
#            guildembeds = {}
#        if not guildembeds:
#            number = 1
#        else:
#            number = sorted(list(guildembeds.keys()),reverse=True)[0] + 1
#        await ctx.send(f"Embed number #{number} created for this server.",embed=embed)
#        guildembeds[number] = embed.to_dict()
#        embeds[str(ctx.guild.id)] = guildembeds
#        json.dump(embeds,f)
#
#    @embed_command.command(name='description')
#    async def embed_command_description(self,ctx,number=int,*,description):
#        f = open('embeds.json','r+')
#        embeds = json.load(f)
#        try:
#            guildembeds = embeds[str(ctx.guild.id)]
#        except:
#            embeds[str(ctx.guild.id)] = {}
#            guildembeds = {}
#        if not guildembeds:
#            await ctx.send("There are no embeds in this server.")
#            return
#        embed = discord.Embed.from_dict(json.loads(guildembeds[number]))
#        embed.description = description
#        await ctx.send(f"Embed #{number} description updated!",embed=embed)
#        guildembeds[number] = dict(embed.to_dict())
#        embeds[str(ctx.guild.id)] = guildembeds
#        json.dump(embeds,f)

cogs = ['Ouija','Owner','Mod','Other']
for cog in cogs:
    exec(f'bot.add_cog({cog}(bot))')

try:
    bot.run(TOKEN)
except KeyboardInterrupt:
    logging.info('Shutting Down')
