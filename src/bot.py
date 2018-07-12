import discord
from discord.ext import commands
from secrets import TOKEN

client = commands.Bot(command_prefix="oe")


@client.event
async def on_ready():
    print("Kongo Master Ready!!")

client.run(TOKEN)
