from urllib.request import urlopen
import io

import discord
from discord.ext import commands

import memegenerator

class Misc:
    @commands.command()
    async def highfive(self, ctx):
        """
        Give Yutu a high-five
        """
        await ctx.send('{0.mention} :pray: {1.mention}'.format(ctx.me, ctx.author))

    @commands.command()
    async def cute(self, ctx, user: discord.Member = None):
        """
        Tell someone they are cute!

        Tells a user that you think they are cute, if you don't give a user, then Yutu will let you know that you are cute.
        """
        if user is None:
            first = ctx.me
            second = ctx.author
        else:
            first = ctx.author
            second = user
        post = discord.Embed(description='**{0.display_name}** thinks that **{1.display_name}** is cute!'.format(first,
                                                                                                                 second))
        post.set_image(url="https://i.imgur.com/MuVAkV2.gif")
        await ctx.send(embed=post)

    @commands.command(hidden=True)
    async def soulpact(self, ctx):
        post = discord.Embed()
        post.description = "Please **{0.display_name}**, give me your soul?\nYou don't need it right?".format(ctx.author)
        post.set_thumbnail(url=ctx.me.avatar_url)
        await ctx.send(embed=post)

    @commands.command()
    async def meme(self, ctx, user: discord.Member, *args):
        async with ctx.typing():
            print(user.avatar_url_as(format="png"))
            av = urlopen(user.avatar_url_as(format="png"))
            img = io.BytesIO()
            msg_text = " ".join(args)
            top = msg_text.split("|")[0].strip()
            bottom = msg_text.split("|")[1].strip()
            memegenerator.make_meme(top, bottom, av, img)
            await ctx.send(file=discord.File(img))
