import collections
import itertools

import discord
from discord.ext import commands

from agithub.GitHub import GitHub

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
    async def request(self, ctx: commands.Context, *, feature):
        """
        Requests a feature from the author, do not abuse
        """
        msg = "Request from {}:\n".format(ctx.author.mention) + feature
        await ctx.bot.pm_owner(content=msg)
        await ctx.message.add_reaction("✅")

    @commands.command()
    async def changelog(self, ctx: commands.Context):
        """
        Get a log of what has changed in Yutu
        """
        status, commits = GitHub().repos.harkonenbade.yutu.commits.get(per_page=10)
        if status == 200:
            await ctx.send(content="```Changelog:\n{}```".format("\n".join(["- {}".format(c['commit']['message'])
                                                                            for c in commits])))
        else:
            await ctx.send(content="Error: Cannot reach github")

    @commands.command(hidden=True)
    @can_manage()
    async def chatshare(self, ctx: commands.Context):
        def grouper(n, iterable):
            it = iter(iterable)
            while True:
                chunk = tuple(itertools.islice(it, n))
                if not chunk:
                    return
                yield chunk

        async with ctx.typing():
            tracking = await ctx.send(content="Scanning channels...")

            chat_log = collections.defaultdict(lambda: 0)
            for channel in ctx.guild.text_channels:
                await tracking.edit(content="Scanning channel: {}".format(channel.name))
                async for msg in channel.history(limit=None):
                    chat_log[msg.author] += 1
            total_msgs = sum(chat_log.values())
            msg_ranks = ['{} - {} - {} - {:0.2f}%'.format(pos + 1, usr, msgs, (msgs/total_msgs)*100)
                         for pos, (usr, msgs) in enumerate(sorted(chat_log.items(), key=lambda item: item[1], reverse=True))]
            await ctx.send(content="```Rank - Name - Total Messages - Percent Messages```")
            for chk in grouper(10, msg_ranks):
                await ctx.send(content="```{}```".format("\n".join(chk)))
            await tracking.delete()