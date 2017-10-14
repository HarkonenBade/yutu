import discord
from discord.ext import commands

TAKE_A_MOMENT = "https://i.imgur.com/4rM92UL.gif"
KALI = 142764404872708096

class KaliCommands:
    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def kalistop(self, ctx: commands.Context):
        """
        Kali is being too intense
        """
        kali = ctx.bot.get_user(KALI)
        post = discord.Embed(description="{0.mention} Stop, take a moment and be mindful.".format(kali))
        post.set_image(url=TAKE_A_MOMENT)
        await ctx.send(embed=post)
