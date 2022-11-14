from datetime import datetime
import discord
import random
import time
from discord import Color
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord.utils import get
from func import *
from dotenv import load_dotenv
load_dotenv()
token = os.getenv("TOKEN")

# Moderation Levels - NOT RELEVANT ANYMORE
# 0 = Common User
# 1 = Bot-Moderator
# 2 = Bot-Admin
# 3 = Bot Superuser
# 4 = Bot Owner

# Gold prices

rickroll_price = 270
change_nickname_price = 1900

# Gold wins

gold_on_message = 1
guess_win = 100


main_guild = 403275615827918878 #931690259555680256
ver = 2.0
intents = discord.Intents.all()
intents.members = True
intents.guilds = True
bot = commands.Bot(command_prefix=".", intents=intents)
bot.remove_command('help')


def getALLCMDS():
    commandList = []
    for i in bot.commands:
        commandList.append(i)
    return commandList


@bot.event
async def on_ready():
    start = time.perf_counter()
    #getALLCMDS()
    createTableinDB()
    createTableinDB2()
    createTableinDB3()
    for i in bot.guilds:
        print(i.name)
        #usr_lst = []
        #for member in i.members:
        #    Common_User1 = [member.id, member.name, 100, 0, 1, 0]
        #    usr_lst.append(Common_User1)
        #Common_User.massInitializationNEW(usr_lst)
        #time.sleep(2)
    #end = time.perf_counter()
    #print(f"Needed {end-start} to initialize")
    print('logged in as {0.user}'.format(bot))
    await bot.change_presence(activity=discord.Game(name="On toilet -> Doing your mom"))
    


@bot.event
async def on_command_error(*args, **kwargs):
    print("Error occured!")
    pass


### Disabled -> inactive/detained users cant use bot-commands ###

#@bot.event
#async def on_command(ctx, *message):
#    if int(isActive(ctx.author)) == 1:
#        await bot.process_commands(message)
#    else:
#        await ctx.send(f"{ctx.author} You banned from using Bot commands!")


@bot.event
async def on_message(message):
    #Bot_SU.addGoldToUser(message.author, gold_on_message)
    if Bot_SU.getActivity(message.author) == 0:
        return
    else:
        await bot.process_commands(message)
        


@bot.event
async def on_member_join(member):
    guild = bot.get_guild(main_guild)
    await member.send(f"__Welcome__ to the guild: [{guild}] {member}")
    Common_User1 = Common_User(member.id, member.name, 100, 0, 1, 0)
    Common_User1.initializeUsersDB()


#@bot.command()
#async def ping(ctx):
#    #@jit(target_backend='cuda')
#    def ping():
#        start = time.perf_counter()
#        a = 0
#        for i in range(200000000):
#            a += i
#        print(f"Time needed {time.perf_counter() - start}")
#        return a
#    ping()


@bot.command(name='DISABLEDcmd', pass_context=True)
async def SUInfo(ctx):
    return
    if Bot_SU.checkSu(ctx.author) == 1:
        help_embed = discord.Embed(title=f"**Superuser info**", icon_url=bot.user.avatar_url, color=Color.red())
        help_embed.set_thumbnail(url='https://cdn.pixabay.com/photo/2013/07/13/13/41/bash-161382__340.png')
        help_embed.add_field(name=f'```Bot-Moderator```', value='Required for moderation', inline=True)
        help_embed.add_field(name=f'```Bot-Superuser```', value='Can add and remove Gold. Commands: gold+ testuser 100 and gold- testuser 100', inline=True)
        await ctx.send(embed=help_embed)


@bot.command(name='suhelp', pass_context=True)
async def SUHelp(ctx):
    if Bot_SU.checkSu(ctx.author) == 1:
        help_embed = discord.Embed(title=f"**Superuser command list**", color=Color.red())
        help_embed.set_thumbnail(url='https://cdn.pixabay.com/photo/2015/02/13/09/47/question-634903__340.png')
        help_embed.add_field(name=f'```gold+```', value=f'Add gold to a user.\n Usage: {bot.command_prefix}gold+ mention/ID ammount', inline=True)
        help_embed.add_field(name=f'```gold-```', value=f'Remove gold from a user.\n Usage: {bot.command_prefix}gold- mention/ID ammount', inline=True)
        await ctx.send(embed=help_embed)


@bot.command(name='help', pass_context=True)
async def helpBasic(ctx):
    help_embed = discord.Embed(title=f"**HELP COMMAND** :small_orange_diamond: Version: {ver}", color=Color.red())
    help_embed.set_thumbnail(url=bot.user.avatar.url)
    help_embed.add_field(name=f'__{bot.command_prefix}useful__', value=':compass:', inline=False)
    help_embed.add_field(name=f'__{bot.command_prefix}eco__', value=':coin:', inline=False)
    help_embed.add_field(name=f'__{bot.command_prefix}fun__', value=':new_moon_with_face:', inline=False)
    help_embed.add_field(name=f'__{bot.command_prefix}mod__', value=':hammer_and_pick:', inline=False)
    help_embed.add_field(name=f'__{bot.command_prefix}admin__', value=':gear:', inline=False)
    help_embed.set_footer(text=f'PLEASE RUN -> {bot.command_prefix}initall <- AFTER ADDING THE BOT', icon_url='https://cdn.pixabay.com/photo/2013/04/01/09/02/important-98442__340.png')
    await ctx.send(embed=help_embed)


@bot.command(name='useful', pass_context=True)
async def helpCommandEconmonics(ctx):
    help_embed = discord.Embed(title=f"**COMMANDS-USEFUL** :small_orange_diamond: PREFIX= {bot.command_prefix}", color=Color.red())
    help_embed.set_thumbnail(url='https://cdn.pixabay.com/photo/2017/03/21/02/00/information-2160912__340.png')
    help_embed.add_field(name='```serverinfo```', value=f'Shows info about the server.\n Usage: {bot.command_prefix}serverinfo', inline=True)
    help_embed.add_field(name='```profile```', value=f'Shows a users bot-profile.\n Usage: {bot.command_prefix}profile (mention/ID)', inline=True)
    help_embed.add_field(name='```getmods```', value=f'Shows all Bot-Moderators in the server.\n Usage: {bot.command_prefix}getrole (mention/ID)', inline=True)
    await ctx.send(embed=help_embed)


@bot.command(name='eco', pass_context=True)
async def helpCommandEconmonics(ctx):
    help_embed = discord.Embed(title=f"**COMMANDS-ECONOMY** :small_orange_diamond: PREFIX= {bot.command_prefix}", color=Color.red())
    help_embed.set_thumbnail(url='https://cdn.pixabay.com/photo/2014/11/01/22/33/gold-513062__340.jpg')
    help_embed.add_field(name='```bal```', value=f'Check your Gold balance.\n Usage: {bot.command_prefix}bal', inline=True)
    help_embed.add_field(name='```check```', value=f'Check another users Gold balance.\n Usage: {bot.command_prefix}check mention/ID', inline=True)
    help_embed.add_field(name='```share```', value=f'Share Gold with another user.\n Usage: {bot.command_prefix}share mention/ID AMMOUNT', inline=True)
    #help_embed.add_field(name='```gold+```', value=f'Give gold to a user.\nRequirements: Bot-Moderator\nUsage: {bot.command_prefix}gold+ mention/ID ammount', inline=True)
    #help_embed.add_field(name='```gold-```', value=f'Remove gold from a user.\nRequirements: Bot-Moderator\nUsage: {bot.command_prefix}role- mention/ID ammount', inline=True)
    help_embed.add_field(name='```guess```', value=f'Guess a number 1-20 and win {guess_win} Gold.\n Usage: {bot.command_prefix}guess NUM', inline=True)
    help_embed.add_field(name='```rob```', value=f'Attempt to rob another user at your own risk.\n Usage: {bot.command_prefix}rob mention/ID', inline=True)
    help_embed.add_field(name='```risk```', value=f'Risk some gold to possible win gld (gambling).\n Usage: {bot.command_prefix}risk AMMOUNT', inline=True)
    await ctx.send(embed=help_embed)


@bot.command(name='fun', pass_context=True)
async def helpCommandEconmonics(ctx):
    help_embed = discord.Embed(title=f"**COMMANDS-FUN** :small_orange_diamond: PREFIX= {bot.command_prefix}", color=Color.red())
    help_embed.set_thumbnail(url='https://cdn.pixabay.com/photo/2021/05/31/07/12/dogecoin-6298018_960_720.png')
    help_embed.add_field(name='```dice```', value=f'Roll a dice (1-6).\n Usage: {bot.command_prefix}dice', inline=True)
    help_embed.add_field(name='```square```', value=f'square a number.\n Usage: {bot.command_prefix}square NUM', inline=True)
    help_embed.add_field(name='```rickroll```', value=f'Rickroll another user. Gold cost= {rickroll_price}.\n Usage: {bot.command_prefix}rickroll mention/ID', inline=True)
    help_embed.add_field(name='```cn```', value=f'Change another users nickname. Gold cost= {change_nickname_price}.\n Usage: {bot.command_prefix}cn mention/ID newNickname', inline=True)
    await ctx.send(embed=help_embed)


@bot.command(name='mod', pass_context=True)
async def helpCommandEconmonics(ctx):
    help_embed = discord.Embed(title=f"**COMMANDS-MODERATOR** :small_orange_diamond: PREFIX= {bot.command_prefix}", color=Color.red())
    help_embed.set_thumbnail(url='https://cdn.pixabay.com/photo/2013/07/12/18/00/socialism-152783__340.png')
    help_embed.add_field(name='```purge```', value=f'Purge messages.\nUsage: {bot.command_prefix}purge AMMOUNT', inline=True)
    help_embed.add_field(name='```ban```', value=f'Ban a user.\n Usage: {bot.command_prefix}ban mention/ID', inline=True)
    help_embed.add_field(name='```unban```', value=f'Unban a user.\n Usage: {bot.command_prefix}unban mention/ID', inline=True)
    help_embed.add_field(name='```kick```', value=f'Kick a user.\n Usage: {bot.command_prefix}kick mention/ID', inline=True)   
    help_embed.add_field(name='```role+```', value=f'Add a specific role to a user.\n Usage: {bot.command_prefix}role+ mention/ID role/roleID', inline=True)
    help_embed.add_field(name='```role-```', value=f'Remove a specific role from a user.\n Usage: {bot.command_prefix}role+ mention/ID role/roleID', inline=True)
    help_embed.add_field(name='```rolecolour```', value=f'Change the colour of a role.\n Usage: {bot.command_prefix}rolecolour role/ID [hexadecimal=0xFFFF00]', inline=True)
    help_embed.set_footer(text=f'!!! Required: Bot-Moderator !!!', icon_url='https://cdn.pixabay.com/photo/2013/04/01/09/02/important-98442__340.png')
    await ctx.send(embed=help_embed)


@bot.command(name='admin', pass_context=True)
async def helpCommandEconmonics(ctx):
    help_embed = discord.Embed(title=f"**COMMANDS-ADMIN** :small_orange_diamond: PREFIX= {bot.command_prefix}", color=Color.red())
    help_embed.set_thumbnail(url='https://cdn.pixabay.com/photo/2015/12/10/16/39/shield-1086702__340.png')
    help_embed.add_field(name='```addmod```', value=f'Add a new Bot-Moderator (Admin required).\n Usage: {bot.command_prefix}addmod mention/ID', inline=True)
    help_embed.add_field(name='```delmod```', value=f'Remove a Bot-Moderator (Admin required).\n Usage: {bot.command_prefix}delmod mention/ID', inline=True)
    help_embed.add_field(name='```initall```', value=f'Initialize all server members to the database (15s cooldown) (required).\n Usage: {bot.command_prefix}initall', inline=True)
    help_embed.set_footer(text=f'!!! Required: ADMINISTRATOR !!!', icon_url='https://cdn.pixabay.com/photo/2013/04/01/09/02/important-98442__340.png')
    await ctx.send(embed=help_embed)


@bot.command(name='serverinfo', pass_context=True)
async def showServerinfo(ctx):
    creationTime = ctx.guild.created_at.strftime("%d/%m/%y")
    serverinfo_embed = discord.Embed(title=f"**SERVERINFO** :globe_with_meridians:", url=ctx.guild.icon.url, color=Color.red())
    serverinfo_embed.set_thumbnail(url="https://cdn.pixabay.com/photo/2016/06/26/23/32/information-1481584__340.png")
    serverinfo_embed.add_field(name='Name', value=f'{ctx.guild.name}\n--------------------', inline=True)
    serverinfo_embed.add_field(name='Server-ID', value=f'{ctx.guild.id}\n--------------------', inline=True)
    serverinfo_embed.add_field(name='Owner', value=f'{ctx.guild.owner.name}#{ctx.guild.owner.discriminator}/{ctx.guild.owner_id}\n--------------------', inline=True)
    serverinfo_embed.add_field(name='Channelcount (text)', value=f'{len(ctx.guild.text_channels)}\n--------------------', inline=True)
    serverinfo_embed.add_field(name='Channelcount (voice)', value=f'{len(ctx.guild.voice_channels)}\n--------------------', inline=True)
    serverinfo_embed.add_field(name='Channelcount (all)', value=f'{len(ctx.guild.text_channels)+len(ctx.guild.voice_channels)}\n--------------------', inline=True)
    serverinfo_embed.add_field(name='Rolecount', value=f'{len(ctx.guild.roles)}\n--------------------', inline=True)
    serverinfo_embed.add_field(name='Membercount', value=f'{ctx.guild.member_count}\n--------------------', inline=True)
    serverinfo_embed.add_field(name='Created at', value=f'{creationTime}\n--------------------', inline=True)
    serverinfo_embed.set_footer(text=f'Requested by: {ctx.author.name}/{ctx.author.id}')
    await ctx.send(embed=serverinfo_embed)


@bot.command(name='profile', pass_context=True)
async def checkUserinfo(ctx, user: discord.Member=None):
    if user is None:
        creationTime = ctx.author.created_at.strftime("%d/%m/%y")
        x = Bot_Moderator.isMod(ctx.guild, ctx.author)
        userinfo_embed = discord.Embed(title=f'**USERINFO  -->  {ctx.author.name}#{ctx.author.discriminator}**', color=Color.red())
        userinfo_embed.set_thumbnail(url=ctx.author.avatar.url)
        userinfo_embed.add_field(name='Name', value=ctx.author.name, inline=True)
        userinfo_embed.add_field(name='Tag', value=f'#{ctx.author.discriminator}', inline=True)
        userinfo_embed.add_field(name='ID', value=ctx.author.id, inline=True)
        userinfo_embed.add_field(name='Is-Moderator', value=x, inline=True)
        userinfo_embed.add_field(name='Gold', value=getCurrentBalance(ctx.author), inline=True)
        userinfo_embed.add_field(name='Acc Created at', value=creationTime, inline=True)
        userinfo_embed.add_field(name='Avatar', value=ctx.author.avatar.url, inline=True)
        userinfo_embed.set_footer(text=f'Requested by: {ctx.author.name}/{ctx.author.id}')
        await ctx.send(embed=userinfo_embed)
    else:
        creationTime = user.created_at.strftime("%d/%m/%y")
        x = Bot_Moderator.isMod(ctx.guild, user)
        userinfo_embed = discord.Embed(title=f'**USERINFO  -->  {user.name}#{user.discriminator}**')
        userinfo_embed.set_thumbnail(url='https://cdn.pixabay.com/photo/2017/11/10/05/48/user-2935527__340.png')
        userinfo_embed.add_field(name='Name', value=user.name, inline=True)
        userinfo_embed.add_field(name='Tag', value=f'#{user.discriminator}', inline=True)
        userinfo_embed.add_field(name='ID', value=user.id, inline=True)
        userinfo_embed.add_field(name='is-Moderator', value=x, inline=True)
        userinfo_embed.add_field(name='Gold', value=getCurrentBalance(user), inline=True)
        userinfo_embed.add_field(name='Acc Created at', value=creationTime, inline=True)
        userinfo_embed.add_field(name='Avatar', value=user.avatar.url, inline=True)
        userinfo_embed.set_footer(text=f'Requested by: {ctx.author.name}/{ctx.author.id}')
        await ctx.send(embed=userinfo_embed)



@bot.command(name='role+', pass_context=True)
async def addRole(ctx, user: discord.Member, role: discord.Role):
    if Bot_Moderator.isMod(ctx.guild, ctx.author):
        await ctx.message.delete()
        await user.add_roles(role)
        await ctx.send(f'Added {user.mention} to {role} :green_circle:')
        print(f"{ctx.author}/{ctx.author.id} added role: {role}/{role.id} --> to user: {user}/{user.id}")


@bot.command(name='role-', pass_context=True)
async def removeRole(ctx, user: discord.Member, role: discord.Role):
    if Bot_Moderator.isMod(ctx.guild, ctx.author):
        await ctx.message.delete()
        await user.remove_roles(role)
        await ctx.send(f'Removed {user.mention} from {role} :green_circle:')


@bot.command(name='ban', pass_context=True)
async def banMember(ctx, user: discord.Member, *args):
    if Bot_Moderator.isMod(ctx.guild, ctx.author):
        await ctx.message.delete()
        reasonBan = ' '.join(args)
        await user.ban(reason=reasonBan)
        await ctx.send(f'{user.name}#{user.discriminator} was banned :green_circle:')
        await user.send(f'You was banned from {ctx.guild.name}. Reason: {reasonBan}.')
        print(f"{ctx.author}/{ctx.author.id} banned user: {user}/{user.id}")


@bot.command(name='kick', pass_context=True)
async def kickMember(ctx, user: discord.Member, *args):
    if Bot_Moderator.isMod(ctx.guild, ctx.author):
        await ctx.message.delete()
        reasonKick = ' '.join(args)
        await user.kick(reason=reasonKick)
        await ctx.send(f'{user.name}#{user.discriminator} was kicked :green_circle:')
        await user.send(f'You was kicked from {ctx.guild.name}. Reason: {reasonKick}.')
        print(f"{ctx.author}/{ctx.author.id} kicked user: {user}/{user.id}")


@bot.command(name='unban', pass_context=True)
async def unbanMember(ctx, user: discord.User):
    if Bot_Moderator.isMod(ctx.guild, ctx.author):
        await ctx.message.delete()
        await ctx.guild.unban(user)
        await ctx.send(f'Unbanned {user.name}#{user.discriminator} from the guild :green_circle:')
        print(f"{ctx.author}/{ctx.author.id} unbanned user: {user}/{user.id}")


@bot.command(name='square', pass_context=True)
async def mathSquare(ctx, num):
    if int(num) <= 9999999999:
        await ctx.send(int(num)*int(num))


@bot.command(name='sqroot', pass_context=True)
async def squareRoot(ctx, num):
    if int(num) <= 9999999999:
        await ctx.send(int(num)**0.5)

@commands.cooldown(1, 15, commands.BucketType.guild)
@bot.command(name='initall', pass_context=True)
@commands.has_permissions(administrator=True)
async def initialize_all_members(ctx):
    await ctx.send("Initializing... This can take some time.")
    start_time = time.perf_counter()
    usr_lst = []
    for member in ctx.guild.members:
        Common_User1 = [member.id, member.name, 100, 0, 1, 0]
        usr_lst.append(Common_User1)
        #Common_User.initializeUsersDB(Common_User1)
        #print(Common_User1)
    Common_User.massInitializationNEW(usr_lst)
    end_time = time.perf_counter()
    print(f"Time needed for initializating {len(usr_lst)} Members: {end_time - start_time}")
    await ctx.send(f"Initialization completed. Initializated __{len(usr_lst)}__ Members :green_circle:")

    
#@jit(target_backend='cuda', forceobj=True)
#def initialize_all_members1(users):
#    for member in users:
#        print(member.id)
#        Common_User.initializeUsersDB(member)
    

@commands.cooldown(1, 15, commands.BucketType.guild)
@bot.command(name='initallSU')
async def initialize_all_members(ctx):
    if Bot_SU.checkSu(ctx.author) == 1:
        await ctx.send("Initializing... This can take some time.")
        start_time = time.perf_counter()
        usr_lst = []
        for member in ctx.guild.members:
            Common_User1 = [(member.id, member.name, 100, 0, 1, 0)]
            usr_lst.append(Common_User1)
            #Common_User.initializeUsersDB(Common_User1)
            #print(Common_User1)
        Common_User.massInitializationNEW(usr_lst)
        end_time = time.perf_counter()
        print(f"Time needed for initializating {len(usr_lst)} Members: {end_time - start_time}")
        await ctx.send(f"Initialization completed. Initializated __{len(usr_lst)}__ Members :green_circle:")


@bot.command(name='getmods', pass_context=True)
async def getModerationLevel(ctx, user: discord.Member=None):
    moderators = Bot_Moderator.modList(ctx.guild)
    mods = [i for i in moderators for i in i]
    modMentions = []
    for i in mods:
        modMentions.append(f"<@{i}>")
    if modMentions:
        servermods_embed = discord.Embed(title=f"**MODERATORS** :hammer_pick:", url=ctx.guild.icon.url, color=Color.red())
        servermods_embed.add_field(name='active moderators:', value="\n".join(modMentions), inline=True)
        await ctx.send(embed=servermods_embed)
    else:
        await ctx.send("No active server moderations!")
    

@bot.command(name='addmod', pass_context=True)
@commands.has_permissions(administrator=True)
async def initialize_Moderator(ctx, user: discord.Member):
    if Bot_Moderator.addMod(user, ctx.guild) == 0:
        print(f"{ctx.author}/{ctx.author.id} initialized a new Moderator {user}/{user.id}.")
        await ctx.send(f"Added new Bot-Moderator: {user.mention} :green_circle:")
    elif Bot_Moderator.addMod(user, ctx.guild) == 1:
        await ctx.send(f"{user.mention} is already a server mod!")


@bot.command(name='delmod', pass_context=True)
@commands.has_permissions(administrator=True)
async def delete_Moderator(ctx, user: discord.Member):
    if Bot_Moderator.deleteMod(user, ctx.guild) == 0:
        await ctx.send(f"Removed Bot-Moderator: {user.mention} :green_circle:")
    elif Bot_Moderator.deleteMod(user, ctx.guild) == 1:
        await ctx.send(f"{user.mention} is no server mod!")


@bot.command(name='active', pass_context=True)
async def activateMember(ctx, user: discord.Member):
    if int(Bot_SU.getActivity(user)) == 0:
        if  int(Bot_SU.checkSu(ctx.author)) == 1 and int(Bot_SU.checkSu(user)) == 0 and ctx.author != user and Bot_SU.checkSu(ctx.author) == 1 and Bot_SU.reactivate(user) == 0:
            await ctx.send(f"{user.mention} is now allowed to use Bot commands")
        else:
            await ctx.send(f"{ctx.author.mention} You dont have permission (Bot-Admin) or the target is equal or above you.")
    else:
        await ctx.send("This user is already allowed to use Bot commands!")


@bot.command(name='detain', pass_context=True)
async def detainMember(ctx, user: discord.Member):
    if int(Bot_SU.getActivity(user)) == 1:
        if  int(Bot_SU.checkSu(ctx.author)) == 1 and int(Bot_SU.checkSu(user)) == 0 and ctx.author != user and Bot_SU.checkSu(ctx.author) == 1 and Bot_SU.setInactive(user) == 0:
            await ctx.send(f"{user.mention} is now banned from using special Bot commands")
        else:
            await ctx.send(f"{ctx.author.mention} You dont have permission (Bot-Superuser) or the target is equal or above you.")
    else:
        await ctx.send("This user is already banned from using Bot commands!")


@bot.command(name='activity', pass_context=True)
async def checkActivityStatus(ctx, user:discord.Member):
    if int(Bot_SU.checkSu(ctx.author)) == 1:
        if int(Bot_SU.getActivity(user)) == 1:
            await ctx.send(f"{user.mention} is allowed to use Bot commands.")
        else:
            await ctx.send(f"{user.mention} is banned from using Bot commands.")
    else:
        await ctx.send(f"{ctx.author.mention} You dont have permission (Bot-Superuser) or the target is equal or above you.")

@bot.command(name='reset0', pass_context=True)
@commands.is_owner()
async def resetALL(ctx):
    Bot_Owner.resetUsers()
    Bot_Owner.resetRes()
    Bot_Owner.resetMod()
    createTableinDB()
    createTableinDB2()
    createTableinDB3
    print(f"Databases resetted!!! --> By user:{ctx.author}/{ctx.author.id}")
    await ctx.send("ALL db resetted! :green_circle:")


@bot.command(name='gold+', pass_context=True)
async def addGold(ctx, user: discord.Member, ammount):
    if int(Bot_SU.checkSu(ctx.author)) == 1 and Bot_SU.addGoldToUser(user, ammount) == 0:
        await ctx.send(f"Added ammount: {ammount} to user:{user.mention} :green_circle:")
        print(f"{ctx.author} added {ammount} to {user}:{user.id}")
    else:
        await ctx.send("You need to be a 'BOT-Superuser' to run this command, or the maximum (99999999 Gold) is reached")

@bot.command(name='gold-', pass_context=True)
async def addGold(ctx, user: discord.Member, ammount):
    if int(Bot_SU.checkSu(ctx.author)) == 1 and Bot_SU.deductGoldFromUser(user, ammount) == 0:
        await ctx.send(f"Reduced ammount: {ammount} from user:{user.mention} :green_circle:")
        print(f"{ctx.author} reduced {ammount} from {user}:{user.id}")
    else:
        await ctx.send("You need to be a 'BOT-Superuser' to run this command. Info: You cant pass 0 Gold")


@bot.command(name='bal', pass_context=True)
async def checkBalance(ctx):
    ammount = getCurrentBalance(ctx.author)
    await ctx.send(f"Balance of {ctx.author.mention}= {ammount} Gold")
 

@bot.command(name='check', pass_context=True)
async def checkBalanceUser(ctx, user: discord.Member):
    ammount = getCurrentBalance(user)
    await ctx.send(f"Balance of {user.mention}= {ammount} Gold")

@bot.command(name='share', pass_context=True)
async def shareGold(ctx, user: discord.Member, ammount):
    if int(ammount) >= 10:
        goldTransacting(ctx.author, user, ammount)
        #if getCurrentBalance(ctx.author) >= int(ammount):
            #ownerCommandDeduceGold(ctx.author, ammount)
            #ownerCommandaddGold(user, ammount)
        print(f"Transaction: {ctx.author} shared {ammount} with {user}.")
        await ctx.send(f"You gifted {user.mention} {ammount} Gold.")
        #else:
            #await ctx.send("Not enough Gold!")
    else:
        await ctx.send(f"Ammount needs to be 10 or larger!")


@bot.command(name='rob', pass_context=True)
async def robUser(ctx, user: discord.Member):
    truefalse = random.randint(0, 1)
    randomNUM = random.randint(25, 1000)
    if getCurrentBalance(user) != 0:
        if truefalse == 0:
            if getCurrentBalance(ctx.author) >= randomNUM:
                Bot_SU.deductGoldFromUser(ctx.author, randomNUM)
                Bot_SU.addGoldToUser(user, randomNUM)
                print(f"{ctx.author}/{ctx.author.id} tried to rob {user}/{user.id} but failed. He paid {randomNUM}")
                await ctx.send(f"Robbery failed! Some gold was deduced from you and gifted to the target! {randomNUM} Gold")
            else:
                randomNUM = getCurrentBalance(ctx.author)
                Bot_SU.deductGoldFromUser(ctx.author, randomNUM)
                Bot_SU.addGoldToUser(user, randomNUM)
                print(f"{ctx.author}/{ctx.author.id} tried to rob {user}/{user.id} but failed. He paid {randomNUM}")
                await ctx.send(f"Robbery failed! Some gold was deduced from you and gifted to the target! {randomNUM} Gold")
        elif truefalse == 1:
            if getCurrentBalance(user) >= randomNUM:
                Bot_SU.addGoldToUser(ctx.author, randomNUM)
                Bot_SU.deductGoldFromUser(user, randomNUM)
                print(f"{ctx.author}/{ctx.author.id} robbed {user}/{user.id} and got {randomNUM} Gold.")
                await ctx.send(f"You robbed {randomNUM} from {user.mention}.")
            else:
                randomNUM = getCurrentBalance(user)
                Bot_SU.addGoldToUser(ctx.author, randomNUM)
                Bot_SU.deductGoldFromUser(user, randomNUM)
                print(f"{ctx.author}/{ctx.author.id} robbed {user}/{user.id} and got {randomNUM} Gold.")
                await ctx.send(f"You robbed {randomNUM} from {user.mention}.")
        else:
            await ctx.send("You cant rob from a user that has 0 Gold!")
    else:
        await ctx.send(f"{ctx.author} You arent allowed to use this command!")


@bot.command(name='dice', pass_context=True)
async def diceRoll(ctx):
    r = random.randint(1, 6)
    await ctx.send(f"You rolled a {r}")


@bot.command(name='rickroll', pass_context=True)
async def rickrollUser(ctx, user: discord.Member):
    userBalance = getCurrentBalance(ctx.author)
    if userBalance >= rickroll_price:
        await ctx.message.delete()
        await ctx.send(f"You got rickrolled {user.mention}! Attacker paid {rickroll_price} Gold. https://c.tenor.com/VFFJ8Ei3C2IAAAAM/rickroll-rick.gif")
        Bot_SU.deductGoldFromUser(ctx.author, rickroll_price)
        print(f"{ctx.author}/{ctx.author.id} used 'rickrolled' command (price={rickroll_price} Gold) on {user}/{user.id}.")
    else:
        await ctx.send(f"You are too poor to use this command {ctx.author.mention}. Cost: {rickroll_price}, Your balance: {userBalance}. __Missing gold = {rickroll_price-userBalance}__")
    
@bot.command(name='cn', pass_context=True)
async def changeNickname(ctx, user: discord.Member, *args):
        newNickname = ' '.join(args)
        if ctx.guild.id in Bot_Moderator.modlist(ctx.guild):
            await ctx.send(f"{ctx.author.mention} Changing nicknames of Bot-Moderators or higher is not permitted!")
            await ctx.message.delete()
            await user.edit(nick=newNickname)
            await ctx.send(f"{user.mention} successfully changed :green_circle:")
            print(f"{ctx.author}/{ctx.author.id} used 'changenick' command on {user}/{user.id}. New nickname: {newNickname}")
        else:
            await ctx.send(f"{ctx.author} You arent allowed to use this command!")

@bot.command(name='guess', pass_context=True)
async def guessNum(ctx, num):
    rnum = random.randint(1, 20)
    if int(num) == rnum:
        Bot_SU.addGoldToUser(ctx.author, guess_win)
        await ctx.send(f"You won. You earned {guess_win} Gold :)")
    else:
        await ctx.send(f"No luck. Maybe next time?! Number was {rnum}.")


@bot.command(name='risk', pass_context=True)
async def riskGold(ctx, ammount):
    if getCurrentBalance(ctx.author) >= int(ammount):
        factor = random.randint(0, 4)
        if factor != 4:
            Bot_SU.deductGoldFromUser(ctx.author, int(ammount))
            await ctx.send(f'{ctx.author.mention} you lost {int(ammount)} Gold')
        else:
            Bot_SU.addGoldToUser(ctx.author, int(ammount)*4)
            await ctx.send(f'{ctx.author.mention} you won {int(ammount)*4} Gold!')
    else:
        await ctx.send(f'You dont have enough gold {ctx.author.mention}!')


@bot.command(name='setGold', pass_context=True)
@commands.is_owner()
async def ownerCommand0(ctx, user: discord.Member, ammount):
        Bot_Owner.setGold(user, ammount)
        print(f"Balance of {user} changed to {ammount} Gold.")
        await ctx.send(f"New balance of {user.mention}= {ammount} Gold")


@bot.command(name='0role+', pass_context=True)
@commands.is_owner()
async def addRole(ctx, user: discord.Member, role: discord.Role):
    await user.add_roles(role)
    await ctx.send(f'Added {user.mention} to {role} :green_circle:')
    print(f"{ctx.author}/{ctx.author.id} added role: {role}/{role.id} --> to user: {user}/{user.id}")


@bot.command(name='0role-', pass_context=True)
@commands.is_owner()
async def removeRole(ctx, user: discord.Member, role: discord.Role):
    await user.remove_roles(role)
    await ctx.send(f'Removed {user.mention} from {role} :green_circle:')


@bot.command(name='addmod0', pass_context=True)
@commands.is_owner()
async def ownerCommand00(ctx, user: discord.Member):
    if Bot_Moderator.addMod(user, ctx.guild) == 0:
        await ctx.send(f"Added new Bot-Moderator {user}.")
        print(f"Added new Bot-Moderator {ctx.guid.id}-{user}/{user.id}.")


@bot.command(name='delmod0', pass_context=True)
@commands.is_owner()
async def ownerCommand00(ctx, user: discord.Member):
    if Bot_Moderator.delMod(user, ctx.guild) == 0:
        await ctx.send(f"Added new Bot-Moderator {user}.")
        print(f"Removed Bot-Moderator {ctx.guid.id}-{user}/{user.id}.")


@bot.command(name='addSU', pass_context=True)
@commands.is_owner()
async def ownerCommand000(ctx, user: discord.Member):
    if Bot_Owner.addSuperuser(user) == 0:
        print(f"Added new Bot-Superuser {user}.")
        await ctx.send(f"Added new Bot-Superuser {user}.")

@bot.command(name='delSU', pass_context=True)
@commands.is_owner()
async def ownerCommand0000(ctx, user: discord.Member):
    if Bot_Owner.deleteSuperuser(user) == 0:
        print(f"Removed Bot-Superuser {user}.")
        await ctx.send(f"Removed Bot-Superuser {user}.")


@bot.command(name='ban0', pass_context=True)
@commands.is_owner()
async def ownerCommand00000(ctx, user: discord.Member, *args):
    await ctx.message.delete()
    reasonBan = ' '.join(args)
    await user.ban(reason=reasonBan)
    await ctx.send(f'{user} was banned :green_circle:')
    await user.send(f'You was banned from {ctx.guild.name}. Reason: {reasonBan}.')
    print(f"{ctx.author}/{ctx.author.id} banned user: {user}/{user.id}")
   

@bot.command(name='rolecolour', pass_context=True)
async def changeRoleColour(ctx, role: discord.Role, colour: discord.Colour):
    if Bot_Moderator.isMod(ctx.guild, ctx.author):
        await role.edit(colour=colour)
        await ctx.send(f"Changed colour of {role.name} to {colour}")


@bot.command(name='purge', pass_context=True)
async def purgeMessages(ctx, num):
    return await ctx.send("Command temporary disabled")
    if Bot_Moderator.isMod(ctx.guild, ctx.author):
        await ctx.message.delete()
        await ctx.channel.purge(limit=int(num))
        await ctx.send(f"Deleted {num} messages :green_circle:")



#@bot.command(name='getAllSU', pass_context=True)
#@commands.is_owner()
#async def getUsersOfModerationLevel(ctx, modLevel):
#        users = []
#        users1 = getAllUsersOfModLevel(modLevel)
#        for i in users1:
#            users.append(i)
#        await ctx.send('\n'.join(users))







# https://discord.com/api/oauth2/authorize?client_id=1013334885143945216&permissions=8&scope=bot

bot.run("YOUR-TOKEN")