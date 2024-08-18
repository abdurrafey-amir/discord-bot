#token
import os
from dotenv import load_dotenv
load_dotenv()

import nextcord
from nextcord.ext import commands
import random

#errors
# import logging
# logging.basicConfig(level=logging.INFO)

token = os.getenv('TOKEN')

test_guild_id = 1265600620056936511
intents = nextcord.Intents.all()

bot = commands.Bot(intents=intents, command_prefix='!')

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

bot.run(token)