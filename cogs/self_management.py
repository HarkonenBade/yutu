import asyncio

import discord
from discord.utils import get
from discord.ext import commands


class SelfManagement:
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

    @commands.command(aliases=['pronoun'])
    async def pronouns(self, ctx: commands.Context, *, pronouns):
        """
        Use to set your pronouns
        
        Enter any number of the following after the command, seperated by spaces:
        he, she, they, it
        """
        roles = {"he": get(ctx.guild.roles, name="he/him"),
                 "she": get(ctx.guild.roles, name="she/her"),
                 "they": get(ctx.guild.roles, name="they/them"),
                 "it": get(ctx.guild.roles, name="it/its")}

        try:
            roles_add = [roles[p] for p in pronouns.lower().split(" ")]
        except KeyError:
            raise commands.BadArgument()
        roles_remove = list(set(roles.values())-set(roles_add))
        await ctx.author.add_roles(*roles_add)
        await ctx.author.remove_roles(*roles_remove)
        await ctx.send("Ok {0.mention}, I have updated your pronoun roles.".format(ctx.author))
