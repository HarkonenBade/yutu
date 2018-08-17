import asyncio

import discord
from discord.utils import get
from discord.ext import commands


class selfmanagement:
    @commands.command()
    async def imsalty(self, ctx: commands.Context):
        """
        Grants you access to the rwde channels
        """
        if get(ctx.guild.roles, name="no salt") in ctx.author.roles:
            await ctx.send("{0.mention}, you are not allowed to give yourself the salty role.".format(ctx.author))
            return

        salty = get(ctx.guild.roles, name="im salty")
        if salty in ctx.author.roles:
            await ctx.send("But {0.mention}, you are already salty.".format(ctx.author))
        else:
            await ctx.author.add_roles(salty, reason="Added by ~imsalty command.")
            await ctx.send("Ok {0.mention}, Granting you access to #rwde and #misc_rwde".format(ctx.author))

    @commands.command()
    async def spoilme(self, ctx: commands.Context):
        """
        Grants you access to the spoiler channels
        """
        if get(ctx.guild.roles, name="no spoilers") in ctx.author.roles:
            await ctx.send("{0.mention}, you are not allowed to give yourself the spoil'd role.".format(ctx.author))
            return

        spoild = get(ctx.guild.roles, name="spoil'd")
        if spoild in ctx.author.roles:
            await ctx.send("But {0.mention}, you have already been spoiled.".format(ctx.author))
        else:
            await ctx.author.add_roles(spoild, reason="Added by ~spoilme command.")
            await ctx.send("Ok {0.mention}, Granting you access to #rwby_spoilers and #rwde_spoilers".format(ctx.author))

    @commands.command()
    async def imlewd(self, ctx: commands.Context):
        """
        Grants you access to the NSFW channels
        """
        DECLARATION = "I assert that I am over the age of 18"
        if get(ctx.guild.roles, name="no lewd") in ctx.author.roles:
            await ctx.send("{0.mention}, you are not allowed to give yourself the nwde role.".format(ctx.author))
            return

        nwde = get(ctx.guild.roles, name="im nwde")
        if nwde in ctx.author.roles:
            await ctx.send("But {0.mention}, you are already nwde.".format(ctx.author))
        else:
            await ctx.send("Please confirm you are over 18. "
                           "Please reply to this message with the following declaration."
                           "\"{}\"".format(DECLARATION))

            try:
                def check(msg):
                    return (msg.author == ctx.author and
                            msg.channel == ctx.channel and
                            DECLARATION in msg.content)
                await ctx.bot.wait_for("message", check=check, timeout=30)
            except asyncio.TimeoutError:
                await ctx.send("Your request has timed out, please try again.")
            else:
                await ctx.author.add_roles(nwde, reason="Added by ~imlewd command.")
                await ctx.send("Ok {0.mention}, Granting you access to #nwde and #dickposting".format(ctx.author))

    @commands.command()
    async def ventilateme(self, ctx: commands.Context):
        """
        Grants you access to the vent channel
        """
        if get(ctx.guild.roles, name="no vent") in ctx.author.roles:
            await ctx.send("{0.mention}, you are not allowed to give yourself the vent role.".format(ctx.author))
            return

        vent = get(ctx.guild.roles, name="im venty")
        if vent in ctx.author.roles:
            await ctx.send("But {0.mention}, you have already been ventilated.".format(ctx.author))
        else:
            await ctx.author.add_roles(vent, reason="Added by ~ventilateme command.")
            await ctx.send("Ok {0.mention}, Granting you access to #vent".format(ctx.author))

    @commands.command()
    async def gethistorical(self, ctx: commands.Context):
        """
        Grants you access to the #histcourse channel
        """
        hist = get(ctx.guild.roles, name="history buff")
        if hist in ctx.author.roles:
            await ctx.send("But {0.mention}, you are already historical.".format(ctx.author))
        else:
            await ctx.author.add_roles(hist, reason="Added by ~gethistorical command.")
            await ctx.send("Ok {0.mention}, Granting you access to #histcourse".format(ctx.author))

    @commands.command(aliases=['pronoun'])
    async def pronouns(self, ctx: commands.Context, *, pronouns):
        """
        Use to set your pronouns
        
        Enter any number of the following after the command, seperated by spaces:
        he, she, they, it, they/she, they/he
        """
        if not hasattr(self.pronouns, "roles"):
            self.pronouns.roles = {"he": get(ctx.guild.roles, name="he/him"),
                                   "he/him": get(ctx.guild.roles, name="he/him"),
                                   "she": get(ctx.guild.roles, name="she/her"),
                                   "she/her": get(ctx.guild.roles, name="she/her"),
                                   "they": get(ctx.guild.roles, name="they/them"),
                                   "they/them": get(ctx.guild.roles, name="they/them"),
                                   "it": get(ctx.guild.roles, name="it/its"),
                                   "it/its": get(ctx.guild.roles, name="it/its"),
                                   "they/she": get(ctx.guild.roles, name="they/she"),
                                   "they/he": get(ctx.guild.roles, name="they/he")}

        try:
            roles_add = {self.pronouns.roles[p] for p in pronouns.lower().split(" ")}
        except KeyError:
            raise commands.BadArgument()
        roles_remove = set(self.pronouns.roles.values())-roles_add
        await ctx.author.add_roles(*list(roles_add))
        await ctx.author.remove_roles(*list(roles_remove))
        await ctx.send("Ok {0.mention}, I have updated your pronoun roles.".format(ctx.author))

    @commands.command()
    async def boxme(self, ctx: commands.Context):
        """
        Put yourself in timeout.
        """
        timeout = get(ctx.guild.roles, name="timeout")
        await ctx.author.add_roles(timeout)
        await ctx.send("Ok {0.mention}, putting you in timeout.".format(ctx.author))

    @commands.command()
    async def games(self, ctx: commands.Context, *, games):
        """
        Use to set your gaming platforms

        Enter any number of the following after the command, seperated by spaces:
        PC, PS3, XBone, Switch
        """
        if not hasattr(self.games, "roles"):
            self.games.roles = {"pc": get(ctx.guild.roles, name="PC gaymer"),
                                "ps3": get(ctx.guild.roles, name="PS gaymer"),
                                "xbone": get(ctx.guild.roles, name="XBone gaymer"),
                                "switch": get(ctx.guild.roles, name="Switch gaymer")}

        try:
            roles_add = {self.games.roles[g] for g in games.lower().split(" ")}
        except KeyError:
            raise commands.BadArgument()
        roles_remove = set(self.games.roles.values()) - roles_add
        await ctx.author.add_roles(*list(roles_add))
        await ctx.author.remove_roles(*list(roles_remove))
        await ctx.send("Ok {0.mention}, I have updated your games roles.".format(ctx.author))
