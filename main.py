#token
import os
from dotenv import load_dotenv
load_dotenv()

import nextcord
from nextcord.ext import commands

#errors
import logging
logging.basicConfig(level=logging.INFO)

token = os.getenv('TOKEN')

test_guild_id = 1265600620056936511

bot = commands.Bot()

@bot.event
async def on_ready():
    print(f'logged in as {bot.user}')

@bot.slash_command(description="first slash cmd", guild_ids=[test_guild_id])
async def hello(interaction: nextcord.Interaction):
    await interaction.send("Hello!")


bot.run(token)