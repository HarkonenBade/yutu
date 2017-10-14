import discord
from discord.ext import commands

TAKE_A_MOMENT = "https://i.imgur.com/4rM92UL.gif"

class KaliCommands:
    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def kalistop(self, ctx: commands.Context):
        """
        Kali is being too intense
        """
        post = discord.Embed(description="@Kali#3164 Stop, take a moment and be mindful.")
        post.set_image(url=TAKE_A_MOMENT)
        await ctx.send(embed=post)
