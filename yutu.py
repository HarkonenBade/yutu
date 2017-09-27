import discord
from discord.ext.commands import Bot
import json

client = Bot("~", game=discord.Game(name="~help"))

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.command()
async def highfive(ctx):
    '''
    Give Yutu a high-five
    '''
    await ctx.send('{0.mention} :pray: {1.mention}'.format(ctx.me, ctx.author))

if __name__ == "__main__":
    with open("cfg.json") as fh:
        token = json.load(fh)['token']
    client.run(token)
