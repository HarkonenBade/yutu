import asyncio

import discord
from discord.ext import commands

REDEYE_BUN = "https://i.imgur.com/1GCqgcR.png"


class SoulPact:
    @commands.command(hidden=True)
    @commands.has_permissions(kick_members=True)
    async def slay(self, ctx: commands.Context, user: discord.Member):
        if user is None:
            await ctx.e_say("**{author}**, I'm sorry I don't know that person")
        else:
            await ctx.e_say("**{target}**, you have lost your soul privileges.\n"
                            "I withdraw from you the light of the most benevolent bun.",
                            target=user,
                            thumbnail=REDEYE_BUN)
            await ctx.guild.kick(user)

    @commands.command(hidden=True)
    async def souls(self, ctx: commands.Context):
        pactee = discord.utils.find(lambda r: r.name == "pactee", ctx.guild.roles)
        souls = sum(1 for m in ctx.guild.members if pactee in m.roles)
        if souls == 0:
            await ctx.e_say("Souls? I don't have any.\n"
                            "Would you give me yours?")
        elif souls < 10:
            await ctx.e_say("Souls? Oh I have at least {souls}.\n"
                            "Though I'm always happy to accept new additions.",
                            souls=souls)
        else:
            await ctx.e_say("I think I have at least {souls}.\n"
                            "The power is really quite *intoxicating*.",
                            souls=souls,
                            thumbnail=REDEYE_BUN)

    @commands.command(hidden=True)
    async def soulpact(self, ctx: commands.Context):
        pactee = discord.utils.find(lambda r: r.name == "pactee", ctx.guild.roles)
        if pactee in ctx.author.roles:
            await ctx.e_say("Oh **{author}**, you already sold your soul to me.\n*grins*")
        else:
            await ctx.e_say("Please **{author}**, give me your soul?\n"
                            "You don't need it right?\n"
                            "Please say yes!")

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
                await ctx.e_say("*The pact is complete*",
                                thumbnail=REDEYE_BUN)
