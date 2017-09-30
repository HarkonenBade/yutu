import discord
from discord.ext import commands

import youtube_dl


class Jukebox:
    def __init__(self):
        self.vc = None
        self.ytdl = youtube_dl.YoutubeDL({'format': 'bestaudio/best',
                                          'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
                                          'restrictfilenames': True,
                                          'quiet': True,
                                          'no_warnings': True,
                                          'default_search': 'auto',
                                          'source_address': '0.0.0.0'})

    async def extract_info(self, loop, *args, **kwargs):
        return await loop.run_in_executor(None, lambda: self.ytdl.extract_info(*args, **kwargs))

    @commands.group()
    async def jukebox(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            post = discord.Embed()
            post.set_thumbnail(url=ctx.me.avatar_url)
            if ctx.subcommand_passed is None:
                if self.vc is None:
                    self.vc = await ctx.guild.voice_channels[0].connect()
                    post.description = "Ok **{0.display_name}**, I'll join voice.".format(ctx.author)
                else:
                    await self.vc.disconnect()
                    self.vc = None
                    post.description = "Ok **{0.display_name}**, I'll leave voice.".format(ctx.author)
            else:
                post.description = "**{0.display_name}**, I don't understand that.".format(ctx.author)
            await ctx.send(embed=post)

    @jukebox.command(aliases=['yes', 'activate'])
    async def on(self, ctx: commands.Context):
        post = discord.Embed()
        post.set_thumbnail(url=ctx.me.avatar_url)
        if self.vc is None:
            self.vc = await ctx.guild.voice_channels[0].connect()
            post.description = "Ok **{0.display_name}**, I'll join voice.".format(ctx.author)
        else:
            post.description = "**{0.display_name}**, I'm already in voice chat.".format(ctx.author)
        await ctx.send(embed=post)

    @jukebox.command(aliases=['no', 'deactivate'])
    async def off(self, ctx:commands.Context):
        post = discord.Embed()
        post.set_thumbnail(url=ctx.me.avatar_url)
        if self.vc is None:
            post.description = "**{0.display_name}**, I'm not in voice chat.".format(ctx.author)
        else:
            await self.vc.disconnect()
            self.vc = None
            post.description = "Ok **{0.display_name}**, I'll leave voice.".format(ctx.author)
        await ctx.send(embed=post)

    @jukebox.command()
    async def play(self, ctx: commands.Context, url: str):
        post = discord.Embed()
        post.set_thumbnail(url=ctx.me.avatar_url)
        if self.vc is not None:
            info = await self.extract_info(ctx.bot.loop, url, download=False)
            self.vc.play(discord.FFmpegPCMAudio(info['url']))
            post.description = "**{0.display_name}**, playing **{1}**".format(ctx.author, info['title'])
        else:
            post.description = "**{0.display_name}**, I'm not currently in voice.".format(ctx.author)
        await ctx.send(embed=post)

    @jukebox.command()
    async def stop(self, ctx: commands.Context):
        post = discord.Embed()
        post.set_thumbnail(url=ctx.me.avatar_url)
        if self.vc is not None:
            self.vc.stop()
            post.description = "**{0.display_name}**, stopping".format(ctx.author)
        else:
            post.description = "**{0.display_name}**, I'm not currently in voice.".format(ctx.author)
        await ctx.send(embed=post)
