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
