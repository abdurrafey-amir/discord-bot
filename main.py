#token
import os
from dotenv import load_dotenv
load_dotenv()

import nextcord
from nextcord.ext import commands
import random
import asyncio
import json

#errors
# import logging
# logging.basicConfig(level=logging.INFO)

token = os.getenv('TOKEN')

test_guild_id = 1265600620056936511
intents = nextcord.Intents.all()
prefix = '!'
bot = commands.Bot(intents=intents, command_prefix=prefix)

@bot.event
async def on_ready():
    print(f'logged in as {bot.user}')

@bot.slash_command(description="first slash cmd", guild_ids=[test_guild_id])
async def hello(interaction: nextcord.Interaction):
    await interaction.send("Hello!")

@bot.command()
async def test(ctx):
    await ctx.send('test')


@bot.command()
async def choose(ctx, option1, option2):
    options = [option1, option2]
    chosen = random.choice(options)
    await ctx.send(f'i choose `{chosen}`')

@bot.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount: int):
    await ctx.channel.purge(limit=amount)
    message = await ctx.send(f'purged {amount} messages')
    await message.delete(delay=3)

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member:nextcord.Member=None, *, reason=None):
    if member is None:
        em1 = nextcord.Embed(title='❌ Invalid use of the kick command.')
        em1.add_field(name='How to use the kick command.', value=f'`{prefix}kick <@member> <Optional: Reason>`')
        await ctx.send(embed=em1)
        return
    pos1 = ctx.guild.roles.index(ctx.author.top_role)
    pos2 = ctx.guild.roles.index(member.top_role)
    if pos1 == pos2:
            return await ctx.send("Both of you have the same power so I can not kick this user for you!")
    if pos1 < pos2:
            return await ctx.send("This person has more power than you so I can not kick him/her for you!")
    
    
    await member.kick(reason=reason)
    await ctx.send(f'{member.mention} has been kicked!')
    # await member.send(f'You have been kicked from `{ctx.guild.name}` for {reason}.')


@kick.error
async def kick_error(ctx, error):
    if isinstance(error,commands.errors.MissingPermissions):
      await ctx.send('You do not have the permissions to perform this command!')

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member:nextcord.Member=None, *, reason=None):
  
    if member is None:
      em = discord.Embed(title='❌ Invalid use of the ban command.')
      em.add_field(name='How to use the ban command.',value=f'`{prefix}ban <MemberMention> <Optional: Reason>`')
      await ctx.send(embed=em)
      return
  
    pos1 = ctx.guild.roles.index(ctx.author.top_role)
    pos2 = ctx.guild.roles.index(member.top_role)
    if pos1 == pos2:
            return await ctx.send("Both of you have the same power so I can not ban this user for you!")
    if pos1 < pos2:
            return await ctx.send("This person has more power than you so I can not ban him/her for you!")
    await member.ban(reason=reason)
    banem = nextcord.Embed(title='Ban 😮',description=f'{member.mention} was banned For {reason}',color=0xff0000)
    await ctx.send(embed=banem)
    # message = f"You have been banned from `{ctx.guild.name}` for {reason}."
    # await member.send(message)

@ban.error
async def ban_error(ctx, error):
    if isinstance(error,commands.errors.MissingPermissions):
      await ctx.send('You do not have the permissions to perform this command!')




@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    banned_users = ctx.guild.bans()

    async for ban_entry in banned_users:
      user = ban_entry.user
 
      unbanem = nextcord.Embed(title='unban 😮',description=f'@{member} has been unbanned',color=0xff0000)
      if user.name == member:
        await ctx.guild.unban(user)
        await ctx.send(embed=unbanem)
        # await member.send(f'You have been unbanned from `{ctx.guild.name}`!')
        return

@unban.error
async def unban_error(ctx, error):
    if isinstance(error,commands.errors.MissingPermissions):
      await ctx.send('You do not have the permissions to perform this command!')


@bot.command()
@commands.guild_only()
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member: nextcord.Member=None, time2=None, reason=None):
    guild = ctx.guild
    muted_role = nextcord.utils.get(ctx.guild.roles, name="Muted")
    if not muted_role:
      muted_role = await guild.create_role(name="Muted", permissions=nextcord.Permissions(send_messages=False, speak=False))
    if member == None or member == ctx.message.author:
         return await ctx.channel.send("You cannot mute yourself :angry:")
         
    
    if reason == None:
        reason = "For being a jerk."
    pos1 = guild.roles.index(ctx.author.top_role)
    pos2 = guild.roles.index(member.top_role)
    if pos1 == pos2:
        return await ctx.send("Both of you have the same power so I can not mute this user for you!")
    if pos2 > pos1:
        return await ctx.send("This person has more power than you so I can not mute him/her for you!")
    
    if time2 == None:
      await member.add_roles(muted_role)
      embed = nextcord.Embed(description=f"<:tick:893901834010390528> {member} has been muted forever\nReason: {reason}", color=nextcord.Color.from_rgb(67, 181, 130))
      await ctx.send(embed=embed)
    
    time_convert = {"s":1, "m":60, "h":3600,"d":86400}
    tempmute = int(time2[:-1]) * time_convert[time2[-1]]
    await member.add_roles(muted_role)
    embed2 = nextcord.Embed(description=f"<:tick:893901834010390528> {member} has been muted for {time2}\nReason: {reason}", color=nextcord.Color.from_rgb(67, 181, 130))
    await ctx.send(embed=embed2)
    await asyncio.sleep(tempmute)
    await member.remove_roles(muted_role)

@mute.error
async def mute_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have the permission to use this command :angry:")
    else:
      raise error



@bot.command()
@commands.guild_only()
@commands.has_permissions(kick_members=True)
async def unmute(ctx, member: nextcord.Member=None):
    muted_role = nextcord.utils.get(ctx.guild.roles, name="Muted") 
    if member == None or member == ctx.message.author:
         await ctx.channel.send("You cannot unmute yourself :angry:")
         return
    pos1 = ctx.guild.roles.index(ctx.author.top_role)
    pos2 = ctx.guild.roles.index(member.top_role)
    if pos1 == pos2:
            return await ctx.send("Both of you have the same power so I can not unmute this user for you!")
    if pos2 > pos1:
            return await ctx.send("This person has more power than you so I can not unmute him/her for you!")
    if muted_role not in member.roles:
      return await ctx.send("This user is not muted!")
    await member.remove_roles(muted_role)
    await ctx.send("Unmuted this user!")

   
@unmute.error
async def unmute_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have the permission to use this command :angry:")


@bot.command()
@commands.guild_only()
@commands.has_permissions(manage_messages=True)
async def warn(ctx,member:nextcord.Member,*,reason=None):
    with open('warns.json','r') as f:
      wj = json.load(f)
   
  
    if f'{ctx.guild.id}' not in wj:
      wj[f'{ctx.guild.id}'] = {}
      wj[f'{ctx.guild.id}'][f'{member.id}'] = {}
      wj[f'{ctx.guild.id}'][f'{member.id}']['warns'] = []
      wj[f'{ctx.guild.id}'][f'{member.id}']['warns'].append(f'{reason} : Warned by {ctx.author}')
      with open('warns.json','w') as f:
       json.dump(wj,f)
      
      embed = nextcord.Embed(title='Warned User!')
      embed.add_field(name='\u200b', value=f'{member.mention} has been warned for {reason}')
      await ctx.send(embed=embed)
      return

    if f'{member.id}' in wj[f'{ctx.guild.id}']:
      wj[f'{ctx.guild.id}'][f'{member.id}']['warns'].append(f'{reason} : Warned by {ctx.author}')
      embed = nextcord.Embed(title="Warned User!")
      embed.add_field(name='\u200b', value=f'{member.mention} has been warned for {reason}')
      await ctx.send(embed=embed)

    
    if f'{member.id}' not in wj[f'{ctx.guild.id}']:
      wj[f'{ctx.guild.id}'][f'{member.id}'] = {}
      wj[f'{ctx.guild.id}'][f'{member.id}']['warns'] = []
      wj[f'{ctx.guild.id}'][f'{member.id}']['warns'].append(f'{reason} : Warned by {ctx.author}')
      embed = nextcord.Embed(title='Warned User!')
      embed.add_field(name='\u200b', value=f'{member.mention} has been warned for {reason}')
      await ctx.send(embed=embed)

    with open('warns.json','w') as f:
      json.dump(wj,f)


@warn.error
async def warn_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please pass in all requirements!')
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permissions to use this command!")




bot.run(token)