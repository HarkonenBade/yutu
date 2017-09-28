import os
import discord
from discord.ext.commands import Bot, when_mentioned_or

DESCRIPTION = """
Hi, I'm Yutu!
I'm the bot for the Velvet fan discord.
I'm still learning so sorry if I do something wrong.
You can ask my programmer @Harkonen if you want to know more about me.
"""

client = Bot(when_mentioned_or("~"),
             game=discord.Game(name="~help"),
             description=DESCRIPTION)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

client.load_extension("cogs")

if __name__ == "__main__":
    client.run(os.environ['DISCORD_TOKEN'])
