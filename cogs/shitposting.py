import random

import discord
from discord.utils import get
from discord.ext import commands

class ShitPosting(commands.Cog):
    @staticmethod
    async def clapcore(ctx, msg, clapper):
        msg = await commands.clean_content().convert(ctx, msg)
        await ctx.send(content="\n".join(["{0} " + " {0} ".join(line.split(" ")) + " {0}"
                                          for line in msg.split('\n')]).format(clapper))

    @commands.command()
    async def clap(self, ctx: commands.Context, *, msg):
        """
        :clap: your :clap: message :clap: here :clap:
        """
        await self.clapcore(ctx, msg, ":clap:")

    @commands.command()
    async def clpa(self, ctx: commands.Context, *, msg):
        """
        :clpa: your :clpa: message :clpa: here :clpa:
        """
        await self.clapcore(ctx, msg, get(ctx.guild.emojis, name='clpa'))

    @commands.command()
    async def boof(self, ctx: commands.Context, *, msg):
        """
        :boof: your :boof: message :boof: here :boof:
        """
        await self.clapcore(ctx, msg, get(ctx.guild.emojis, name='boof'))

    @commands.command()
    async def obamaclap(self, ctx: commands.Context, *, msg):
        """
        :perish: your :perish: message :perish: here :perish:
        """
        await self.clapcore(ctx, msg, get(ctx.guild.emojis, name='perish'))

    @commands.command()
    async def lewdclap(self, ctx: commands.Context, * , msg):
        """
        Clap a lewd message
        """
        await self.clapcore(ctx, msg, get(ctx.guild.emojis, name='lewd'))

    @commands.command()
    async def blushclap(self, ctx: commands.Context, * , msg):
        """
        Velv is embarrised about your message
        """
        await self.clapcore(ctx, msg, get(ctx.guild.emojis, name='bunblush'))

    @commands.command()
    async def bunclap(self, ctx: commands.Context, *, msg):
        """
        :bun: your :bun: message :bun: here :bun:
        """
        class BunGen():
            bun_list = [get(ctx.guild.emojis, name='peekabun'),
                        get(ctx.guild.emojis, name='peekafrappbun'),
                        get(ctx.guild.emojis, name='peekacarnagebun')]
            def __str__(self):
                return str(random.choice(self.bun_list))

        await self.clapcore(ctx, msg, BunGen())


    @commands.command()
    async def owo(self, ctx: commands.Context, *, msg):
        """
        Say something in a 'cute' way
        """
        msg = await commands.clean_content().convert(ctx, msg)
        transforms = {'na': 'nya',
                      'ne': 'nye',
                      'ni': 'nyi',
                      'nu': 'nyu',
                      'no': 'nyo',
                      'r': 'w',
                      'l': 'w'}
        for src, dst in transforms.items():
            msg = msg.replace(src, dst).replace(src.upper(), dst.upper()).replace(src.title(), dst.title())
        await ctx.send(content=msg)

    @commands.command(aliases=['leet'])
    async def l33t(self, ctx: commands.Context, *, msg):
        """
        L33t m3ss4g1ng
        """
        msg = await commands.clean_content().convert(ctx, msg)
        transforms = {'e': '3',
                      'i': '1',
                      'o': '0',
                      'a': '4',
                      's': '5',
                      'v': '\\\\/',
                      'n': '|\\\\|'}
        for src, dst in transforms.items():
            msg = msg.replace(src.lower(), dst)
        await ctx.send(content=msg)

    @commands.command()
    async def nb(self, ctx: commands.Context, *, msg):
        """
        Make a message more non-binary
        """
        msg = await commands.clean_content().convert(ctx, msg)
        await ctx.send(content=msg.translate({ord('n'): 'nb',
                                              ord('N'): 'NB',
                                              ord('b'): 'nb',
                                              ord('B'): 'NB'}))

    @commands.command()
    async def spiritmiku(self, ctx:commands.Context, number: int = None):
        """
        Find your spirit miku (supply a follower number, or it will use your discord username #number)
        """
        mikunum = ((number if number is not None else int(ctx.author.discriminator)) % 348) + 1
        print(mikunum)
        await ctx.send(content="{}'s Spirit Miku\nhttp://miku.sega.jp/mega39s/img/module/module_{}.png".format(ctx.author, mikunum))
