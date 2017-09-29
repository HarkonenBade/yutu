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
