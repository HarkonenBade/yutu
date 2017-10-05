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
        await ctx.e_say("Ok **{author}**\n*SYSTEM RESTARTING*")
        ctx.bot.loop.stop()

    @commands.command()
    async def request(self, ctx: commands.Context, *args):
        """
        Requests a feature from the author, do not abuse
        """
        msg = "Request from {}:\n".format(ctx.author.mention) + " ".join(args)
        await ctx.bot.get_user(ctx.bot.owner_id).send(content=msg)
        await ctx.message.add_reaction("✅")
