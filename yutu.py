import discord
from discord.ext.commands import Bot, when_mentioned_or
import json

client = Bot(when_mentioned_or("~"), game=discord.Game(name="~help"))


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

client.load_extension("cogs")

if __name__ == "__main__":
    with open("cfg.json") as fh:
        token = json.load(fh)['token']
    client.run(token)
