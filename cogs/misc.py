import hashlib

import discord
from discord.ext import commands


class Misc:
    @commands.command()
    async def highfive(self, ctx: commands.Context):
        """
        Give Yutu a high-five
        """
        await ctx.send('{0.mention} :pray: {1.mention}'.format(ctx.me, ctx.author))

    @commands.command()
    async def cute(self, ctx: commands.Context, user: discord.Member = None):
        """
        Tell someone they are cute!

        Tells a user that you think they are cute, if you don't give a user,
        then Yutu will let you know that you are cute.
        """
        if user is None:
            first = ctx.me
            second = ctx.author
        else:
            first = ctx.author
            second = user
        post = discord.Embed(
            description='**{0.display_name}** thinks that **{1.display_name}** is cute!'.format(first, second))
        post.set_image(url="https://i.imgur.com/MuVAkV2.gif")
        await ctx.send(embed=post)

    @commands.command()
    async def rate(self, ctx: commands.Context, *args):
        """
        Ask Yutu to rate a thing
        """
        sample = " ".join(args)
        hasher = hashlib.sha256()
        hasher.update(sample.lower().encode("UTF-8"))
        rate = int(hasher.hexdigest(), 16) % 1001
        msg = discord.Embed()
        msg.description = "**{0.display_name}** gives **{1}** a rating of **{2}/100**".format(ctx.me,
                                                                                              sample,
                                                                                              rate/10.0)
        msg.set_thumbnail(url=ctx.me.avatar_url)
        await ctx.send(embed=msg)

    @commands.command(aliases=['hugs'])
    async def hug(self, ctx: commands.Context, user: discord.Member = None):
        """
        Give someone a hug
        """
        if user is None:
            first = ctx.me
            second = ctx.author
        else:
            first = ctx.author
            second = user
        post = discord.Embed(
            description="**{0.display_name}** gives **{1.display_name}** a warm hug".format(first, second)
        )
        post.set_image(url="https://i.imgur.com/RDdGYgK.gif")
        post.set_thumbnail(url=first.avatar_url)
        await ctx.send(embed=post)
