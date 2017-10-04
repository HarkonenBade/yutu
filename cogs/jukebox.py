import asyncio

import discord
from discord.ext import commands

import youtube_dl


class Jukebox:
    def __init__(self):
        self.vc = None
        self.ytdl = youtube_dl.YoutubeDL({'format': 'bestaudio/best',
                                          'outtmpl': 'cache/%(id)s.%(ext)s',
                                          'restrictfilenames': True,
                                          'quiet': True,
                                          'no_warnings': True,
                                          'default_search': 'auto',
                                          'source_address': '0.0.0.0'})

    async def extract_info(self, loop, *args, **kwargs):
        return await loop.run_in_executor(None, lambda: self.ytdl.extract_info(*args, **kwargs))

    async def next(self):
        pass

    def play(self, loop: asyncio.BaseEventLoop, name):
        self.vc.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(name)),
                     after=lambda err: loop.call_soon(self.next))

    @commands.group()
    async def jukebox(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            if ctx.subcommand_passed is None:
                if self.vc is None:
                    self.vc = await ctx.guild.voice_channels[0].connect()
                    await ctx.e_say("Ok **{author}**, I'll join voice.")
                else:
                    await self.vc.disconnect()
                    self.vc = None
                    await ctx.e_say("Ok **{author}**, I'll leave voice.")
            else:
                await ctx.e_say("**{author}**, I don't understand that.")

    @jukebox.command(aliases=['yes', 'activate'])
    async def on(self, ctx: commands.Context):
        if self.vc is None:
            self.vc = await ctx.guild.voice_channels[0].connect()
            await ctx.e_say("Ok **{author}**, I'll join voice.")
        else:
            await ctx.e_say("**{author}**, I'm already in voice chat.")

    @jukebox.command(aliases=['no', 'deactivate'])
    async def off(self, ctx: commands.Context):
        if self.vc is None:
            await ctx.e_say("**{author}**, I'm not in voice chat.")
        else:
            await self.vc.disconnect()
            self.vc = None
            await ctx.e_say("Ok **{author}**, I'll leave voice.")

    @jukebox.command()
    async def play(self, ctx: commands.Context, url: str):
        post = discord.Embed()
        post.set_thumbnail(url=ctx.me.avatar_url)
        if self.vc is not None:
            post.description = "**{0}**, loading...".format(ctx.author)
            msg = await ctx.send(embed=post)
            info = await self.extract_info(ctx.bot.loop, url, download=True)
            self.play(ctx.bot.loop, self.ytdl.prepare_filename(info))
            post.description = "**{0}**, playing **{1}**".format(ctx.author, info['title'])
            await msg.edit(embed=post)
        else:
            post.description = "**{0}**, I'm not currently in voice.".format(ctx.author)
            await ctx.send(embed=post)

    @jukebox.command()
    async def stop(self, ctx: commands.Context):
        if self.vc is not None:
            self.vc.stop()
            await ctx.e_say("**{author}**, stopping")
        else:
            await ctx.e_say("**{author}**, I'm not currently in voice.")

    @jukebox.command()
    async def volume(self, ctx: commands.Context, vol: int = None):
        if self.vc.source is not None:
            if vol is not None:
                vol = max(0, min(100, vol))
                self.vc.source.volume = vol/100.0

