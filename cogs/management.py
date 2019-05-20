import collections
import itertools
import io
import json
import gzip
import datetime

import discord
from discord.ext import commands

from agithub.GitHub import GitHub

def can_manage():
    def pred(ctx: commands.Context):
        return ctx.bot.is_owner(ctx.author)
    return commands.check(pred)

class Manage(commands.Cog):
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

    @commands.command(hidden=True)
    @can_manage()
    async def archive(self, ctx: commands.Context):
        class Enc(json.JSONEncoder):
            def default(self, o):
                if isinstance(o, discord.Message):
                    ret = {
                        "tts": o.tts,
                        "author": o.author,
                        "content": o.content,
                        #"embeds": o.embeds,
                        "id": o.id,
                        "attachments": o.attachments,
                        "pinned": o.pinned,
                        "reactions": o.reactions,
                        "created_at": o.created_at.isoformat(),
                    }
                    if o.edited_at is not None:
                        ret["edited_at"] = o.edited_at.isoformat()
                    return ret
                elif isinstance(o, discord.Member):
                    return {
                        "id": o.id,
                        "joined_at": o.joined_at.isoformat(),
                        "display_name": o.display_name,
                        "avatar": o.avatar_url,
                        "username": o.name + "#" + o.discriminator,
                    }
                elif isinstance(o, discord.Attachment):
                    return {
                        "id": o.id,
                        "url": o.url,
                    }
                elif isinstance(o, discord.Reaction):
                    return {
                        "emoji": o.emoji,
                        "count": o.count,
                    }
                elif isinstance(o, discord.Emoji):
                    return {
                        "id": o.id,
                        "name": o.name,
                        "url": o.url,
                    }
                return super().default(o)

        chname = ctx.channel.name
        async with ctx.typing():
            await ctx.message.delete()
            status = await ctx.send(content="Archiving {}...".format(chname))
            out = io.BytesIO()
            stream = gzip.GzipFile(fileobj=out, mode="a")
            stat_update = 0
            async for msg in ctx.channel.history(limit=None):
                stream.write(json.dumps(msg, cls=Enc).encode("utf-8"))
                stream.write('\n'.encode("utf-8"))
                stat_update += 1
                if stat_update % 1000 == 0:
                    delta = datetime.datetime.now() - msg.created_at
                    await status.edit(content="Archiving {}, {} remaining...".format(chname, delta))
            stream.close()
            out.seek(0)
            await status.delete()
            await ctx.send(content="Archived {} containing {} messages".format(chname, stat_update),
                           file=discord.File(out, filename="{}.gz".format(chname)))
