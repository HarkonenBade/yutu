import discord
from discord.utils import get
from discord.ext import commands


def is_role_reqs():
    ROLE_REQUESTS = 360514141271752704
    def chk(ctx: commands.Context):
        return ctx.channel.id == ROLE_REQUESTS
    return commands.check(chk)


class SelfManagement:
    @commands.command()
    @is_role_reqs()
    async def imsalty(self, ctx: commands.Context):
        """
        Grants you access to the rwde channels
        
        Can only be used in #role_requests
        """
        salty = get(ctx.guild.roles, name="salty")
        if salty in ctx.author.roles:
            await ctx.send("But {0.mention}, you are already salty.".format(ctx.author))
        else:
            await ctx.author.add_roles(salty, reason="Added by ~imsalty command.")
            await ctx.send("Ok {0.mention}, Granting you access to #rwde and #misc_rwde")

    @commands.command()
    @is_role_reqs()
    async def spoilme(self, ctx: commands.Context):
        """
        Grants you access to the spoiler channels
        
        Can only be used in #role_requests
        """
        spoild = get(ctx.guild.roles, name="spoil'd")
        if spoild in ctx.author.roles:
            await ctx.send("But {0.mention}, you have already been spoiled.".format(ctx.author))
        else:
            await ctx.author.add_roles(spoild, reason="Added by ~spoilme command.")
            await ctx.send("Ok {0.mention}, Granting you access to #rwby_spoilers and #rwde_spoilers")

    @commands.command()
    @is_role_reqs()
    async def pronouns(self, ctx: commands.Context, *, pronouns):
        """
        Use to set your pronouns
        
        Enter any number of the following after the command, seperated by spaces:
        he, she, they, it
        
        Can only be used in #role_requests
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
