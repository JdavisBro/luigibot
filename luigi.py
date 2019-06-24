import discord
from discord.ext import commands
import asyncio
import random
import time, datetime
from discord.ext.commands import CommandNotFound
import sys
import logging
import json

logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s', level=logging.INFO)

try:
    open("prefixes.json","x")
    open("prefixes.json","w").write("{}")
    logging.info("prefixes.json created, used to store per server prefixes.")
except:
    logging.info("prefixes.json already exists, unable to create it.")

with open("prefixes.json","r") as f:
    prefixes = json.load(f)

default_prefix = "o!"

async def prefix(bot, message):
    if type(message.channel) is not discord.DMChannel:
        id = str(message.guild.id)
        return prefixes.get(id, default_prefix)
    else:
        return default_prefix

client = commands.Bot(command_prefix=prefix,description="A bot to replicate /r/askouija on Discord!")
TOKEN = sys.argv[1]
channel_names = ["ask-ouija","askouija","ouija","ouijaboard","ask-luigi","askluigi","luigiboard"]
client.startTime = time.time()
update=0
on = {}
client.question = {}
client.answer = {}
client.msg = {}
client.messageembed = {}
client.prevuser = {}
client.origauthor = {}

@client.event
async def on_ready():
    logging.info('Connected to DISCORD as {}'.format(str(client.user)))
    game = discord.Game(name='with my LuigiBoard. o!help')
    await client.change_presence(status=discord.Status.online, activity=game)
    global appinfo, owner
    appinfo = await client.application_info()
    owner = appinfo.owner

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        channel = ctx.channel
        if channel.name in channel_names:
            await ctx.send("Command not found, if you are trying to ask a question use o!ask")
        return
    raise error

def setquestion(channelid,question):
    client.question[channelid] = question

def setanswer(channelid,answer):
    client.answer[channelid] = answer

def setmsg(channelid,msg):
    client.msg[channelid] = msg

def setembed(channelid,messageembed):
    client.messageembed[channelid] = messageembed

def setprevuser(channelid,prevuser):
    client.prevuser[channelid] = prevuser

def setuser(channelid,user):
    client.origauthor[channelid] = user

@client.event
async def on_message(message):
    global on, owner, channel_names
    if type(message.channel) is not discord.DMChannel:
        if message.guild.id not in on.keys():
            on[message.guild.id] = 0
        if on[message.guild.id] != 0:
            if message.channel.name in channel_names:
                if message.author == owner or message.author == message.guild.me:
                    if message.content.startswith("##"):
                        return
                question = client.question[message.guild.id]
                answer = client.answer[message.guild.id]
                msg = client.msg[message.guild.id]
                embed = client.messageembed[message.guild.id]
                prevuser = client.prevuser[message.guild.id]
                user = client.origauthor[message.guild.id]
                length = len(message.content)
                if not message.author.bot:
                    if length == 1:
                        if message.author != user and message.author != prevuser and message.content != '{':
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
                        else:
                            try:
                                await message.delete()
                            except:
                                pass
                    elif message.content == 'space' or message.content == 'Space':
                        if message.author != user and message.author != prevuser:
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
                        else:
                            try:
                                await message.delete()
                            except:
                                pass
                    elif message.content == 'goodbye' or message.content == 'Goodbye':
                        if message.author != user and message.author != prevuser:
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
                        else:
                            try:
                                await message.delete()
                            except:
                                pass
                    elif message.content == 'stopouija':
                        if message.author == owner:
                            on[message.guild.id] = 0
                            logging.info('{} used stopouija to stop the question going on in {}'.format(str(owner),message.guild.name))
                        else:
                            logging.info('A user who is not {} attempted to use stopouija in {}'.format(str(owner),message.guild.name))
                            try:
                                await message.delete()
                            except:
                                pass
                    else:
                        await client.process_commands(message)
                        try:
                            await message.delete()
                        except:
                            pass
                else:
                    await client.process_commands(message)
                    try:
                        await message.delete()
                    except:
                        pass
            else:
                if message.author.bot == False:
                    if message.content.startswith("if you are real say "):
                        send=message.content.replace("if you are real say ","")
                        await message.channel.send("{}, lol".format(send))
                await client.process_commands(message)
        else:
            if message.author.bot == False:
                if message.content.startswith("if you are real say "):
                    send=message.content.replace("if you are real say ","")
                    await message.channel.send("{}, lol".format(send))
                await client.process_commands(message)
    else:
        if message.author.bot == False:
            if message.content.startswith("if you are real say "):
                send=message.content.replace("if you are real say ","")
                await message.channel.send("{}, lol".format(send))
            await client.process_commands(message)

@client.command()
async def ask(ctx,*,question):
    "Asks a question! Can only be used in a channel named 'ask-ouija'"
    global update
    if update == 0:
        if ctx.guild.id not in on.keys():
            on[ctx.guild.id] = 0
        if on[ctx.guild.id] == 0:
            channel = ctx.channel
            user = ctx.author
            if channel.name in channel_names:
                on[ctx.guild.id] = ctx.channel.id
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

@client.command()
@commands.is_owner()
async def exit(ctx):
    'Stops the bot, only usable by the owner.'
    await ctx.send('Goodbye! 👋')
    await client.close()

@client.command()
async def setprefix(ctx,prefixToBeSet="o!"):
    'Sets the command prefix for this server, only usable by a user that has the Manage Server permissions, if the prefix you want contains space put it in "quotes". Defaults to `o!` if no prefix is specified'
    if ctx.author.guild_permissions.manage_guild or ctx.author == ctx.guild.owner:
        prefixes[str(ctx.guild.id)] = prefixToBeSet
        await ctx.send("Prefix for {} set to `{}`".format(ctx.guild.name,prefixToBeSet))
        with open("prefixes.json","w") as f:
            f.write(str(json.dumps(prefixes)))
            f.flush()

@client.command()
async def uptime(ctx):
    'Shows you how long the bot has been online'
    currentTime = time.time()
    uptime = int(round(currentTime - client.startTime))
    uptime = str(datetime.timedelta(seconds=uptime))
    colour = discord.Colour.from_rgb(random.randint(1,255),random.randint(1,255),random.randint(1,255))
    embed = discord.Embed(title="I have been up for", description=uptime, color=colour)
    await ctx.send(embed=embed)

@client.command()
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

@client.command()
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


@client.command()
@commands.is_owner()
async def say(ctx, *, say):
    'Makes the bot say something, only usable by the owner'
    try:
        await ctx.message.delete()
    except:
        pass
    await ctx.channel.trigger_typing()
    await asyncio.sleep(0.2)
    await ctx.send(say.format(ctx))

@client.command()
@commands.is_owner()
async def updatesoon(ctx):
    'Stops new Questions from being asks and shuts down ongoing ouijas after 5 minutes, only usable by the owner'
    ouijasactive = 0
    global on, update
    update = 1
    for channelid in on.values():
        if channelid != 0:
            ouijasactive += 1
            channel = client.get_channel(channelid)
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
            channel = client.get_channel(channelid)
            await channel.send("Shutting Down Ouija.")
            question = client.question[channel.guild.id]
            answer = client.answer[channel.guild.id]
            msg = client.msg[channel.guild.id]
            embed = client.messageembed[channel.guild.id]
            user = client.origauthor[channel.guild.id]
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

@client.command()
@commands.is_owner()
@commands.dm_only()
async def servers(ctx):
    'Lists the servers the bot is in, only usable by the owner in DMs'
    guilds = ''
    for guild in client.guilds:
        guilds += guild.name + '\n'
    await ctx.send(guilds)

client.run(TOKEN)
