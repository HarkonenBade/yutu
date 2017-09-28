import asyncio

import discord
from discord.ext import commands


class SoulPact:
    @commands.command(hidden=True)
    async def soulpact(self, ctx: commands.Context):
        pactee = discord.utils.find(lambda r: r.name == "pactee", ctx.guild.roles)
        post = discord.Embed()
        if pactee in ctx.author.roles:
            post.description = "Oh **{0.display_name}**, you already sold your soul to me.\n*grins*".format(ctx.author)
            post.set_thumbnail(url=ctx.me.avatar_url)
            await ctx.send(embed=post)
        else:
            post.description = ("Please **{0.display_name}**, give me your soul?\n"
                                "You don't need it right?\n"
                                "Please say yes!".format(ctx.author))
            post.set_thumbnail(url=ctx.me.avatar_url)
            await ctx.send(embed=post)

            def check(message: discord.Message):
                return (message.author == ctx.author and
                        message.channel == ctx.channel and
                        (ctx.me in message.mentions or not message.mentions) and
                        "yes" in message.content.lower())

            try:
                await ctx.bot.wait_for('message', check=check, timeout=30)
            except asyncio.TimeoutError:
                await ctx.send(":frowning:")
            else:
                await ctx.author.add_roles(pactee, reason="Soul Pact")
                rsp = discord.Embed()
                rsp.description = "*The pact is complete*"
                rsp.set_thumbnail(url="https://i.imgur.com/1GCqgcR.png")
                await ctx.send(embed=rsp)
