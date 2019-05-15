import discord
from discord.ext import commands
import time
import random
from discord.ext.commands import CommandNotFound
import sys

#hey

TOKEN = sys.argv[1]
client = commands.Bot(command_prefix='o!')
f = open("appcodes.txt")
on = {}
dontallowouija=0
client.question = {}
client.answer = {}
client.msg = {}
client.messageembed = {}
client.prevuser = {}
client.origauthor = {}

@client.event
async def on_ready():
    print('Connection Established!\nConnected to DISCORD as {}'.format(client.user.name))
    game = discord.Game(name='with my LuigiBoard.')
    await client.change_presence(status=discord.Status.online, activity=game)

@client.event
async def on_reconnect():
    print("Reconnected!")

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
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
    global on
    if str(message.channel.id) not in on.keys():
        on[str(message.channel.id)] = 0
    if on[str(message.channel.id)] == 1:
        if message.channel.name == "ask-ouija":
            if message.author.id == 105725338541101056:
                if message.content.startswith("##"):
                    return
        question = client.question[message.channel.id]
        answer = client.answer[message.channel.id]
        msg = client.msg[message.channel.id]
        embed = client.messageembed[message.channel.id]
        prevuser = client.prevuser[message.channel.id]
        user = client.origauthor[message.channel.id]
        length = len(message.content)
        if message.author.bot == False:
            if length == 1:
                if message.author != user:
                    if message.author != prevuser:
                        answer = answer.replace('{}', message.content + '{}')
                        embed.add_field(name='The current answer is:', value='`{}`'.format(answer.replace('{}', '')), inline=False)
                        await message.add_reaction('✅')
                        await msg.edit(embed=embed)
                        embed.clear_fields()
                        prevuser = message.author
                        setprevuser(message.channel.id,prevuser)
                        setanswer(message.channel.id,answer)
                        time.sleep(0.5)
                    else:
                        try:
                            await message.delete()
                        except:
                            pass
                else:
                    try:
                        await message.delete()
                    except:
                        pass
            elif message.content == 'space':
                if message.author != user:
                    if message.author != prevuser:
                        answer = answer.replace('{}', ' {}')
                        embed.add_field(name='The current answer is:', value='`{}`'.format(answer.replace('{}', '')), inline=False)
                        await message.add_reaction('✅')
                        await msg.edit(embed=embed)
                        embed.clear_fields()
                        prevuser = message.author
                        setprevuser(message.channel.id,prevuser)
                        setanswer(message.channel.id,answer)
                        time.sleep(0.5)
                    else:
                        try:
                            await message.delete()
                        except:
                            pass
                else:
                    try:
                        await message.delete()
                    except:
                        pass
            elif message.content == 'goodbye' or message.content == 'Goodbye':
                if message.author != user:
                    on[str(message.channel.id)] = 0
                    setprevuser(message.channel.id,'')
                    embed = discord.Embed(title="We have the answer to {}'s question!".format(user.name), description='The question was `{}`'.format(question), color=2151680)
                    embed.set_author(name='Ouija Question!', url='https://discord.gg/FxFvQye', icon_url='https://www.fjordsafari.com/wp-content/uploads/2016/11/question-mark-4-xxl.png')
                    embed.set_thumbnail(url='https://cdn.discordapp.com/avatars/557320040127397888/5f3d0e0ad8a4a8143d261745fad05f1a.png?size=256')
                    embed.add_field(name='The answer is', value='`{}`'.format(answer).replace('{}', ''), inline=False)
                    msg1 = await message.channel.send("We have the answer to {}'s question!".format(user.mention))
                    await message.channel.send(embed=embed)
                    await msg.delete()
                    time.sleep(0.5)
                    await msg1.delete()
                    answer = ''
                    print('OFF in {}'.format(message.guild.name))
                else:
                    try:
                        await message.delete()
                    except:
                        pass
            elif message.content == 'stopouija':
                if message.author.id == 105725338541101056:
                    on[str(message.channel.id)] = 0
                    print('JdavisBro#2640 used stopouija to stop the question going on in {}'.format(message.guild.name))
                else:
                    print('A user who is not JdavisBro#2640 attempted to use stopouija in {}'.format(message.guild.name))
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

@client.command()
async def ask(ctx,*,question):
    """Asks a question! Can only be used in a channel named 'ask-ouija'"""
    global dontallowouija
    if dontallowouija == 0:
        if str(ctx.message.channel.id) not in on.keys():
            on[str(ctx.message.channel.id)] = 0
        if on[str(ctx.message.channel.id)] != 1:
            channel = ctx.channel
            user = ctx.author
            message = ''
            if channel.name == 'ask-ouija':
                if ctx.guild.me.permissions_in(channel).manage_messages:
                    answer = ''
                    if '{}' in question:
                        answer = question
                    else:
                        answer = '{}'
                    if question != '':
                        embed = discord.Embed(title="A question has come in! Say one letter or 'space' to answer it! ", description='`{}`'.format(question), color=6363163)
                        embed.set_author(name='Ouija Question!', url='https://discord.gg/FxFvQye', icon_url='https://www.fjordsafari.com/wp-content/uploads/2016/11/question-mark-4-xxl.png')
                        embed.set_thumbnail(url='https://cdn.discordapp.com/avatars/557320040127397888/5f3d0e0ad8a4a8143d261745fad05f1a.png?size=256')
                        embed.add_field(name='The current answer is:', value='`{}`'.format(answer.replace('{}', ' ')), inline=False)
                        embed.set_footer(text='Question by {}'.format(user))
                        try:
                            role=discord.utils.get(ctx.guild.roles, name='Luigi')
                            msg1=await ctx.send("{}: {} (in {}) has asked `{}`!".format(role.mention,user.name,ctx.guild.name,question))
                        except:
                            pass
                        msg = await ctx.send(embed=embed)
                        try:
                            await msg.pin()
                        except:
                            pass
                        time.sleep(0.5)
                        try:
                            await msg1.delete()
                        except:
                            pass
                        embed.clear_fields()
                        setuser(ctx.channel.id,user)
                        setquestion(ctx.channel.id,question)
                        setanswer(ctx.channel.id,answer)
                        setembed(ctx.channel.id,embed)
                        setmsg(ctx.channel.id,msg)
                        setprevuser(ctx.channel.id,"")
                        on[str(ctx.message.channel.id)] = 1
                    else:
                        await ctx.send("Hey, you need to ask something!!")
                else:
                    await channel.send("I don't have permissions to manage messages in this channel.")
            else:
                time.sleep(0.5)
                print('Wrong channel')
        else:
            try:
                await ctx.message.delete()
            except:
                pass
            time.sleep(0.5)
            print('already going')
    else:
        await ctx.say("Ouija is not allowed to start as there is an update soon!")

@client.command()
async def exit(ctx):
    'Stops the bot'
    if ctx.author.id == 105725338541101056:
        await ctx.send('Goodbye! 👋')
        await client.change_presence(status=discord.Status.invisible)
        await client.close()

@client.command()
async def role(ctx):
    'Gives you the Luigi role for pings when a new Ouija starts!'
    member = ctx.author
    try:
        discord.utils.get(member.guild.roles, name='Luigi')
    except:
        msg=await ctx.send("This server doesn't have a Luigi role.")
        time.sleep(10)
        await msg.delete()
        return
    msg = await ctx.send('Ok, {} has been given the Luigi role!'.format(ctx.author.name))
    role = discord.utils.get(member.guild.roles, name='Luigi')
    await member.add_roles(role)
    time.sleep(10)
    await msg.delete()

@client.command()
async def unrole(ctx):
    'Removes the Luigi role if you have it (and if it exists in the server)!'
    member = ctx.author
    try:
        discord.utils.get(member.guild.roles, name='Luigi')
    except:
        msg=await ctx.send("This server doesn't have a Luigi role.")
        time.sleep(10)
        await msg.delete()
        return
    msg=await ctx.send('Ok, {} has been removed from the Luigi role!'.format(ctx.author.name))
    member = ctx.author
    role = discord.utils.get(member.guild.roles, name='Luigi')
    await member.remove_roles(role)
    time.sleep(10)
    await msg.delete()

@client.command()
async def say(ctx, *, say):
    if ctx.author.id == 105725338541101056:
        await ctx.message.delete()
        await ctx.channel.trigger_typing()
        time.sleep(0.5)
        await ctx.send(say)

#@client.command()
#@commands.is_owner()
#async def updatesoon(ctx):
#    global dontallowouija
#    dontallowouija==1
#    print(dontallowouija)

@client.command()
@commands.is_owner()
async def servers(ctx):
    servers=''
    for guild in client.guilds:
        servers+=guild.name
        servers+='\n'
    await ctx.send(servers)

#@client.command()
#async def reactors(ctx,msgid,channel: discord.TextChannel,emote: discord.Emoji,randomize=0):
#    msgid=int(msgid)
#    reactions=''
#    reactors=''
#    msg=''
#    react=''
#    history=await channel.history(limit=200).flatten()
#    for message in history:
#        if message.id == msgid:
#            msg=message
#        else:
#            pass
#    reactions=msg.reactions
#    for reaction in reactions:
#        if reaction.emoji==emote:
#            react=reaction
#    users = await react.users().flatten()
#    for user in users:
#        reactors+=user.name
#        reactors+='\n'
#    if randomize!=1:
##        sentmessage=await ctx.send(content=reactors)
#    else:
#        times=1
#        sentmessage=await ctx.send(content="{}{}/10".format(reactors,times))
#        time.sleep(1)
#        for x in range(9):
#            times+=1
#            reactors=''
#            random.shuffle(users)
#            for user in users:
#                reactors+=user.name
#                reactors+='\n'
#            await sentmessage.edit(content="{}{}/10".format(reactors,times))
#            time.sleep(1)
#
#@client.command()
#async def getappcode(ctx):
#    print(type(ctx.channel) is discord.DMChannel)
#    if type(ctx.channel) is discord.DMChannel:
#        global f
#        listatm=eval(f.read())
#        if ctx.author.id not in listatm.keys():
#            while True:
#                userint=random.randint(1000000,9999999)
#                if userint in listatm.values():
#                    print("HOW I SWEAR TO GOD")
#                else:
#                    listatm[ctx.author.id]=userint
#                    fw=open("appcodes.txt","w")
#                    fw.write(str(listatm))
#                    fw.flush()
#                    print(ctx.author.name,"has been given the code",userint)
#                    await ctx.send("Your code is {}".format(userint))
#                    break
#        else:
#            await ctx.send("You already have a code. It's {}".format(listatm[ctx.author.id]))
#
#@client.command()
#@commands.is_owner()
#async def getcodefor(ctx,number: int):
#    global f
#    if type(ctx.channel) is discord.DMChannel:
#        listatm=eval(f.read())
#        if number in listatm.values():
#            for id, userint in listatm.items():
#                if userint == number:
#                    await ctx.send("{} is {}".format(number,client.get_user(id)))

client.run(TOKEN)
