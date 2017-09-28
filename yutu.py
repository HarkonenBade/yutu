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

@client.command()
async def cute(ctx, member: discord.Member = None):
    if member is None:
        first = ctx.me
        second = ctx.author
    else:
        first = ctx.author
        second = member
    post = discord.Embed(description='**{0.name}** thinks that **{1.name}** is cute!'.format(first, second))
    post.set_image(url="https://i.imgur.com/MuVAkV2.gif")
    await ctx.send(embed=post)

if __name__ == "__main__":
    with open("cfg.json") as fh:
        token = json.load(fh)['token']
    client.run(token)
