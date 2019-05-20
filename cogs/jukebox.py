import asyncio
import collections

import discord
from discord.ext import commands

import youtube_dl

QueueEntry = collections.namedtuple("QueueEntry", ['fname', 'title', 'added_by'])

class Jukebox(commands.Cog):
    def __init__(self):
        super().__init__()
        self.vc = None
        self.vol = 100
        self.play_queue = []
        self.ytdl = youtube_dl.YoutubeDL({'format': 'bestaudio/best',
                                          'outtmpl': 'cache/%(id)s.%(ext)s',
                                          'restrictfilenames': True,
                                          'quiet': True,
                                          'no_warnings': True,
                                          'default_search': 'auto',
                                          'source_address': '0.0.0.0'})

    async def extract_info(self, loop, *args, **kwargs):
        return await loop.run_in_executor(None, lambda: self.ytdl.extract_info(*args, **kwargs))

    def next(self, loop):
        if self.play_queue:
            self._play(loop, self.play_queue.pop(0).fname)

    def _play(self, loop: asyncio.BaseEventLoop, name):
        self.vc.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(name), volume=self.vol/100.0),
                     after=lambda err: self.next(loop))

    @commands.group()
    async def jukebox(self, ctx: commands.Context):
        """
        Commands for playing music in voice-chat
        """
        if ctx.invoked_subcommand is None:
            if ctx.subcommand_passed is None:
                await ctx.send(content="I don't understand that. "
                                       "Use `~help jukebox` to find out how to use this command.")

    @jukebox.command(aliases=['yes', 'activate'])
    async def on(self, ctx: commands.Context):
        """
        Make Yutu join voice 
        """
        if self.vc is None:
            self.vc = await ctx.guild.voice_channels[0].connect()
            await ctx.send(content="Ok, I'll join voice.")
        else:
            await ctx.send(content="I'm already in voice chat.")

    @jukebox.command(aliases=['no', 'deactivate'])
    async def off(self, ctx: commands.Context):
        """
        Make Yutu leave voice
        """
        if self.vc is None:
            await ctx.send(content="I'm not in voice chat.")
        else:
            await self.vc.disconnect()
            self.vc = None
            await ctx.send(content="Ok, I'll leave voice.")

    @jukebox.command()
    async def play(self, ctx: commands.Context, url: str = None):
        """
        Start the queue playing, or play a single song by url
        """
        if self.vc is not None:
            if url is None:
                if self.play_queue:
                    self.next(ctx.bot.loop)
                else:
                    await ctx.send(content="You need to give a url to play, or have something queued.")
            else:
                await ctx.message.delete()
                post = discord.Embed()
                post.set_thumbnail(url=ctx.me.avatar_url)
                post.description = "**{0}**, loading...".format(ctx.author)
                msg = await ctx.send(embed=post)
                info = await self.extract_info(ctx.bot.loop, url, download=True)
                self._play(ctx.bot.loop, self.ytdl.prepare_filename(info))
                post.description = "**{0}**, playing **{1}**".format(ctx.author, info['title'])
                await msg.edit(embed=post)
        else:
            await ctx.send(content="I'm not currently in voice. Use `~jukebox on` to make me join.")

    @jukebox.command()
    async def stop(self, ctx: commands.Context):
        """
        Ends the currently playing song
        """
        if self.vc is not None:
            self.vc.stop()
            await ctx.send(content="Stopping")
        else:
            await ctx.send(content="I'm not currently in voice. Use `~jukebox on` to make me join.")

    @jukebox.command()
    async def volume(self, ctx: commands.Context, vol: int = None):
        """
        Set the playback volume between 0-100
        """
        if vol is not None:
            vol = max(0, min(100, vol))
            self.vol = vol
            if self.vc is not None and self.vc.source is not None:
                self.vc.source.volume = vol/100.0
            await ctx.send(content="Setting volume to {}%".format(vol))
        else:
            await ctx.send(content="Volume set to {}%".format(self.vol))

    @jukebox.group(usage=" ", invoke_without_command=True)
    async def queue(self, ctx: commands.Context):
        """
        Manipulate the play queue
        
        If executed with no subcommand it is the same as ~jukebox queue list
        """
        if ctx.invoked_subcommand is None:
            if ctx.subcommand_passed == "queue":
                print("attempting to list")
                await ctx.invoke(self.list)
            else:
                await ctx.send(content="I don't understand that. "
                                       "Use `~help jukebox queue` to find out how to use this command.")

    @queue.command()
    async def add(self, ctx: commands.Context, url: str):
        """
        Add a song to the play queue by url 
        """
        post = discord.Embed()
        post.set_thumbnail(url=ctx.me.avatar_url)
        post.description = "**{0}**, loading...".format(ctx.author)
        msg = await ctx.send(embed=post)
        info = await self.extract_info(ctx.bot.loop, url, download=True)
        self.play_queue.append(QueueEntry(fname=self.ytdl.prepare_filename(info),
                                          title=info['title'],
                                          added_by=ctx.author))
        post.description = "**{0}**, added **{1}** to the queue in place #{2}".format(ctx.author,
                                                                                      info['title'],
                                                                                      len(self.play_queue))
        await msg.edit(embed=post)

    @queue.command()
    async def list(self, ctx: commands.Context):
        """
        List the songs in the play queue
        """
        if self.play_queue:
            await ctx.send(content="```{}```".format("\n".join(["{}: {} - {}".format(i + 1, q.title, q.added_by)
                                                                for i, q in enumerate(self.play_queue)])))
        else:
            await ctx.send(content="Queue is currently empty.")

    @queue.command()
    async def clear(self, ctx: commands.Context):
        """
        Empty the play queue
        """
        self.play_queue.clear()
        await ctx.send(content="Clearing play queue")
