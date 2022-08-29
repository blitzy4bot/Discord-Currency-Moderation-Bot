from distutils import errors
from unicodedata import category
import discord
import random
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord.utils import get
from func import *
from dotenv import load_dotenv
load_dotenv()
token = os.getenv("TOKEN")
# Gold prices

rickroll_price = 10
change_nickname_price = 25

# Gold wins

guess_win  = 12


main_guild = 931690259555680256
ver = 1.0
intents = discord.Intents.default()
intents.members = True
intents.guilds = True
bot = commands.Bot(command_prefix=".", intents=intents)
bot.remove_command('help')



@bot.event
async def on_ready():
    print('logged in as {0.user}'.format(bot))


@bot.event
async def on_command_error(*args, **kwargs):
    print("Error occured!")
    pass

@bot.command()
async def ping(ctx):
    await ctx.send("pong!")

@bot.command(name='help', pass_context=True)
async def helpBasic(ctx):
    help_embed= discord.Embed(title=f"*HELP COMMAND* - Ver={ver}",
    icon_url=bot.user.avatar_url)
    help_embed.add_field(name='__eco__', value=':coin:', inline=True)
    help_embed.add_field(name='__fun__', value=':new_moon_with_face:', inline=True)
    help_embed.add_field(name='__mod__', value=':hammer_and_pick:', inline=True)
    help_embed.add_field(name='__admin__', value=':gear:', inline=True)
    await ctx.send(embed=help_embed)

@bot.command(name='eco', pass_context=True)
async def helpCommandEconmonics(ctx):
    help_embed = discord.Embed(title=f"*COMMANDS-ECONOMY (Page=1/1) __PREFIX='{bot.command_prefix}'__'*",
    icon_url=bot.user.avatar_url)
    help_embed.set_thumbnail(url='https://cdn.pixabay.com/photo/2014/11/01/22/33/gold-513062__340.jpg')
    help_embed.add_field(name='__bal__', value=f'Check your Gold balance.\n Usage: {bot.command_prefix}bal', inline=True)
    help_embed.add_field(name='__check__', value=f'Check another users Gold balance.\n Usage: {bot.command_prefix}check mention/ID', inline=True)
    help_embed.add_field(name='__gold+__', value=f'Give gold to a user.\nRequirements: Bot-Moderator\nUsage: {bot.command_prefix}gold+ mention/ID ammount', inline=True)
    help_embed.add_field(name='__guess__', value=f'Guess a number 1-20.\n Usage: {bot.command_prefix}guess NUM', inline=True)
    help_embed.add_field(name='__gold-__', value=f'Remove gold from a user.\nRequirements: Bot-Moderator\nUsage: {bot.command_prefix}role- mention/ID ammount', inline=True)
    await ctx.send(embed=help_embed)


@bot.command(name='fun', pass_context=True)
async def helpCommandEconmonics(ctx):
    help_embed = discord.Embed(title=f"*COMMANDS-FUN (Page=1/1) __PREFIX='{bot.command_prefix}'__'*",
    icon_url=bot.user.avatar_url)
    help_embed.set_thumbnail(url='https://cdn.pixabay.com/photo/2021/05/31/07/12/dogecoin-6298018_960_720.png')
    help_embed.add_field(name='__dice__', value=f'Roll a dice (1-6).\n Usage: {bot.command_prefix}dice', inline=True)
    help_embed.add_field(name='__square__', value=f'square a number.\n Usage: {bot.command_prefix}square NUM', inline=True)
    help_embed.add_field(name='__rickroll__', value=f'Rickroll another user. Gold cost={rickroll_price}\n Usage: {bot.command_prefix}rickroll mention/ID', inline=True)
    help_embed.add_field(name='__cn__', value=f'Change another users nickname. Gold cost={change_nickname_price}\n Usage: {bot.command_prefix}cn mention/ID newNickname', inline=True)
    await ctx.send(embed=help_embed)


@bot.command(name='mod', pass_context=True)
async def helpCommandEconmonics(ctx):
    help_embed = discord.Embed(title=f"*COMMANDS-MODERATOR (Page=1/1) __PREFIX='{bot.command_prefix}'__'*",
    icon_url=bot.user.avatar_url)
    help_embed.set_thumbnail(url='https://cdn.pixabay.com/photo/2013/07/12/18/00/socialism-152783__340.png')
    help_embed.add_field(name='__ban__', value=f'Ban a user.\n Usage: {bot.command_prefix}ban mention/ID', inline=True)
    help_embed.add_field(name='__unban__', value=f'Unban a user.\n Usage: {bot.command_prefix}unban mention/ID', inline=True)
    help_embed.add_field(name='__kick__', value=f'Kick a user.\n Usage: {bot.command_prefix}kick mention/ID', inline=True)   
    help_embed.add_field(name='__role+__', value=f'Add a specific role to a user.\n Usage: {bot.command_prefix}role+ mention/ID role/roleID', inline=True)
    help_embed.add_field(name='__role-__', value=f'Remove a specific role from a user.\n Usage: {bot.command_prefix}role+ mention/ID role/roleID', inline=True)
    await ctx.send(embed=help_embed)


@bot.command(name='admin', pass_context=True)
async def helpCommandEconmonics(ctx):
    help_embed = discord.Embed(title=f"*COMMANDS-ADMIN (Page=1/1) __PREFIX='{bot.command_prefix}'__'*",
    icon_url=bot.user.avatar_url)
    help_embed.set_thumbnail(url='https://cdn.pixabay.com/photo/2015/12/10/16/39/shield-1086702__340.png')
    help_embed.add_field(name='__addmod__', value=f'Add a new Bot-Moderator.\n Usage: {bot.command_prefix}ban mention/ID', inline=True)
    help_embed.add_field(name='__delmod__', value=f'Remove a Bot-Moderator.\n Usage: {bot.command_prefix}unban mention/ID', inline=True)
    await ctx.send(embed=help_embed)


@bot.event
async def on_member_join(member):
    guild = bot.get_guild(main_guild)
    print(guild)
    #await member.send(f"__Welcome__ to the guild: [{guild.name}] {member}")
    initializeUsers(member)
    

@bot.command(name='role+', pass_context=True)
@has_permissions(manage_roles=True)
async def addRole(ctx, user: discord.Member, role: discord.Role):
    await user.add_roles(role)
    await ctx.send(f'Added {user.mention} to {role} :green_circle:')
    print(f"{ctx.author}/{ctx.author.id} added role: {role}/{role.id} --> to user: {user}/{user.id}")



@bot.command(name='role-', pass_context=True)
@has_permissions(manage_roles=True)
async def removeRole(ctx, user: discord.Member, role: discord.Role):
    await user.remove_roles(role)
    await ctx.send(f'Removed {user.mention} from {role} :green_circle:')


@bot.command(name='ban', pass_context=True)
@has_permissions(kick_members=True)
async def banMember(ctx, user: discord.Member, *args):
    reasonBan = ' '.join(args)
    await user.ban(reason=reasonBan)
    await ctx.send(f'{user.mention} was banned :green_circle:')
    await user.send(f'You was banned from {ctx.guild.name}. Reason: {reasonBan}.')
    print(f"{ctx.author}/{ctx.author.id} banned user: {user}/{user.id}")


@bot.command(name='banOwner', pass_context=True)
@commands.is_owner()
async def banMember(ctx, user: discord.Member, *args):
    reasonBan = ' '.join(args)
    await user.ban(reason=reasonBan)
    await ctx.send(f'{user.mention} was banned :green_circle:')
    await user.send(f'You was banned from {ctx.guild.name}. Reason: {reasonBan}.')
    print(f"{ctx.author}/{ctx.author.id} banned user: {user}/{user.id}")


@bot.command(name='kick', pass_context=True)
@has_permissions(ban_members=True)
async def banMember(ctx, user: discord.Member, *args):
    reasonKick = ' '.join(args)
    await user.kick(reason=reasonKick)
    await ctx.send(f'{user.mention} was kicked :green_circle:')
    await user.send(f'You was kicked from {ctx.guild.name}. Reason: {reasonKick}.')
    print(f"{ctx.author}/{ctx.author.id} kicked user: {user}/{user.id}")


@bot.command(name='unban', pass_context=True)
@has_permissions(ban_members=True)
async def unbanMember(ctx, user: discord.User):
    await ctx.guild.unban(user)
    await ctx.send(f'Unbanned {user.mention} from the guild :green_circle:')
    print(f"{ctx.author}/{ctx.author.id} unbanned user: {user}/{user.id}")


@bot.command(name='square', pass_context=True)
async def mathSquare(ctx, num):
    await ctx.send(int(num)*int(num))


@bot.command(name='sqroot', pass_context=True)
async def squareRoot(ctx, num):
    await ctx.send(int(num)**0.5)


@bot.command(name='initall', pass_context=True)
@commands.is_owner()
async def initialize_all_members(ctx):
    for members in ctx.guild.members:
        initializeUsers(members)
    await ctx.send("Initialization completed :green_circle:")


@bot.command(name='addmod', pass_context=True)
@commands.has_permissions(administrator=True)
async def initialize_Moderator(ctx, user: discord.Member):
    inititalizeMod(user)
    await ctx.send(f"Added new Bot-Moderator: {user.mention} :green_circle:")


@bot.command(name='delmod', pass_context=True)
@commands.has_permissions(administrator=True)
async def initialize_Moderator(ctx, user: discord.Member):
    deleteMod(user)
    await ctx.send(f"Removed Bot-Moderator: {user.mention} :green_circle:")


@bot.command(name='reset0x00', pass_context=True)
@commands.is_owner()
async def resetALL(ctx):
    createTableinDB()
    resetUsers()
    print(f"Databse resetted!!! by user:{ctx.author}/{ctx.author.id}")
    await ctx.send("Users db resetted! :green_circle:")


@bot.command(name='gold+', pass_context=True)
async def addGold(ctx, user: discord.Member, ammount):
    if addGoldtoUser(ctx.author, user, ammount) == 0:
        await ctx.send(f"Added ammount:{ammount} to user:{user.mention} :green_circle:")
        print(f"{ctx.author} added {ammount} to {user}:{user.id}")
    else:
        await ctx.send("You need to be a 'BOT-Moderator' to run this command, or the maximum is reached")

@bot.command(name='gold-', pass_context=True)
async def addGold(ctx, user: discord.Member, ammount):
    if deductGoldfromUser(ctx.author, user, ammount) == 0:
        await ctx.send(f"Reduced ammount:{ammount} from user:{user.mention} :green_circle:")
        print(f"{ctx.author} reduced {ammount} from {user}:{user.id}")
    else:
        await ctx.send("You need to be a 'BOT-Moderator' to run this command. Info: You cant pass 0 Gold")


@bot.command(name='bal', pass_context=True)
async def checkBalance(ctx):
    ammount = getCurrentBalance(ctx.author)
    await ctx.send(f"Balance of {ctx.author.mention}= {ammount} Gold")
 

@bot.command(name='check', pass_context=True)
async def checkBalanceUser(ctx, user: discord.Member):
    ammount = getCurrentBalance(user)
    await ctx.send(f"Balance of {user.mention}= {ammount} Gold")


@bot.command(name='dice', pass_context=True)
async def diceRoll(ctx):
    r = random.randint(1, 6)
    await ctx.send(f"You rolled a {r}")


@bot.command(name='rickroll', pass_context=True)
async def rickrollUser(ctx, user: discord.Member):
    userBalance = getCurrentBalance(ctx.author)
    if userBalance >= rickroll_price:
        await ctx.message.delete()
        await ctx.send(f"You got rickrolled {user.mention}! https://c.tenor.com/VFFJ8Ei3C2IAAAAM/rickroll-rick.gif")
        deductGoldfromUserbyADMIN(ctx.author, rickroll_price)
        print(f"{ctx.author}/{ctx.author.id} used 'rickrolled' command (price={rickroll_price} Gold) on {user}/{user.id}")
    else:
        await ctx.send(f"You are too poor to use this command {ctx.author.mention}. Cost: {rickroll_price}, Your balance: {userBalance}. __Missing gold = {rickroll_price-userBalance}__")
    
    
@bot.command(name='cn', pass_context=True)
async def changeNickname(ctx, user: discord.Member, newNickname):
    userBalance = getCurrentBalance(ctx.author)
    if userBalance >= change_nickname_price:
        await ctx.message.delete()
        await user.edit(nick=newNickname)
        await ctx.send(f"{user.mention} your nickname was secretly changed.")
        deductGoldfromUserbyADMIN(ctx.author, change_nickname_price)
        print(f"{ctx.author}/{ctx.author.id} used 'changenick' command (price={change_nickname_price} Gold) on {user}/{user.id}")
    else:
        await ctx.send(f"You are too poor to use this command {ctx.author.mention}. Cost: {change_nickname_price}, Your balance: {userBalance}. __Missing gold = {change_nickname_price-userBalance}__")


@bot.command(name='guess', pass_context=True)
async def guessNum(ctx, num):
    rnum = random.randint(1, 20)
    if num == rnum:
        ownerComandaddGold(ctx.author, guess_win)
        await ctx.send(f"You won. You earned {guess_win} Gold :)")
    await ctx.send("No luck. Maybe next time?!")





@bot.command(name='setGold', pass_context=True)
@commands.is_owner()
async def ownerCommand0(ctx, user: discord.Member, ammount):
    ownerComandaddGold(user, ammount)
    print(f"Balance of {user} changed to {ammount} Gold.")
    await ctx.send(f"New balance of {user.mention}= {ammount} Gold")


@bot.command(name='setMod', pass_context=True)
@commands.is_owner()
async def ownerCommand00(ctx, user: discord.Member):
    inititalizeMod(user)
    print(f"Added new Bot-Moderator {user}.")
    await ctx.send(f"Added new Bot-Moderator {user}.")






    
    







# https://discord.com/api/oauth2/authorize?client_id=1013334885143945216&permissions=8&scope=bot

bot.run(token)