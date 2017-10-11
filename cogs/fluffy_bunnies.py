import asyncio

import discord
from discord.ext import commands

REDEYE_BUN = "https://i.imgur.com/1GCqgcR.png"
PENTAGRAM = "https://i.imgur.com/L6qiCyv.png"

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
        acolyte = discord.utils.find(lambda r: r.name == "acolyte", ctx.guild.roles)
        souls = sum(1 for m in ctx.guild.members if acolyte in m.roles)
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
    @commands.cooldown(rate=1, per=3600, type=commands.BucketType.guild)
    @commands.guild_only()
    @commands.bot_has_permissions(manage_messages=True)
    async def rite(self, ctx: commands.Context):
        acolyte = discord.utils.find(lambda r: r.name == "acolyte", ctx.guild.roles)
        souls = sum(1 for m in ctx.guild.members if acolyte in m.roles)
        if souls < 20:
            await ctx.e_say("I don't think that will work, I need more power first.",
                            thumbnail=REDEYE_BUN)
        else:
            post = discord.Embed(description="A cold wind races through the channel, "
                                             "and blood red lines start creeping across the floor.")
            post.set_image(url=PENTAGRAM)
            msg = await ctx.send(embed=post)
            await ctx.e_say("Come my acolytes, speak my name and give power to this rite of the most benevolent bun.",
                            thumbnail=REDEYE_BUN)
            power = 0
            participants = set()
            weakening = False
            complete = False
            def mentioned(msg):
                return ctx.me.mentioned_in(msg) and acolyte in msg.author.roles
            while not complete:
                try:
                    m = await ctx.bot.wait_for("message", check=mentioned, timeout=30)
                except asyncio.TimeoutError:
                    if not weakening:
                        await ctx.e_say("The ritual is weakening my acolytes, "
                                        "if you do not add more power soon it will fail.",
                                        thumbnail=REDEYE_BUN)
                        weakening = True
                    else:
                        await msg.delete()
                        await ctx.e_say("It is no good, the power will not hold together. "
                                        "We must try again later.")
                        return
                else:
                    if m.author in participants:
                        await ctx.send(content="You must find your fellow acolytes.")
                    else:
                        power += 1
                        participants.add(m.author)
                        weakening = False
                        if power > 4:
                            complete = True
                        elif power > 3:
                            await ctx.send(content="So close my acolytes.")
                        elif power > 1:
                            await ctx.send(content="Perfect, just a few more acolytes.")
                        else:
                            await ctx.send(content="Yes, now gather more of your fellows.")
            await ctx.e_say("Excellent work my acolytes, you have wrought the blessing of "
                            "the most benevolent bun into this channel.",
                            thumbnail=REDEYE_BUN)
            post.description = ("A rune of shimmering red is engraved into the ground, "
                                "the gaze of the most benevolent bun shines down on {}, "
                                "thanks to the efforts of {}.").format(ctx.channel.mention,
                                                                       ", ".join([u.mention for u in participants]))
            await msg.edit(embed=post)
            await msg.pin()


    @commands.command(hidden=True)
    async def soulpact(self, ctx: commands.Context):
        acolyte = discord.utils.find(lambda r: r.name == "acolyte", ctx.guild.roles)
        if acolyte in ctx.author.roles:
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
                await ctx.author.add_roles(acolyte, reason="Soul Pact")
                await ctx.e_say("*The pact is complete*",
                                thumbnail=REDEYE_BUN)
