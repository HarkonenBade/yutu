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

        salty = get(ctx.guild.roles, name="salty")
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

        roles_add = [roles[p] for p in pronouns.lower().split(" ")]
        roles_remove = list(set(roles.values())-set(roles_add))
        await ctx.author.add_roles(*roles_add)
        await ctx.author.remove_roles(*roles_remove)
        await ctx.send("Ok {0.mention}, I have updated your pronoun roles.".format(ctx.author))
