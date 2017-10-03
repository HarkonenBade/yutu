import discord
from discord.ext import commands


def can_manage():
    def pred(ctx: commands.Context):
        return ctx.bot.is_owner(ctx.author)
    return commands.check(pred)

class Manage:
    @commands.command(hidden=True)
    @can_manage()
    async def restart(self, ctx: commands.Context):
        post = discord.Embed()
        post.description = "Ok **{0.display_name}**\n*SYSTEM RESTARTING*".format(ctx.author)
        post.set_thumbnail(url=ctx.me.avatar_url)
        await ctx.send(embed=post)
        ctx.bot.loop.stop()
