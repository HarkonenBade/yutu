import random

import discord
from discord.ext import commands

TAKE_A_MOMENT = "https://i.imgur.com/4rM92UL.gif"
THATS_GAY = "https://i.imgur.com/w8tbJc5.gif"
KALI = 142764404872708096

class KaliCommands(commands.Cog):
    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def kalistop(self, ctx: commands.Context):
        """
        Kali is being too intense
        """
        kali = ctx.bot.get_user(KALI)
        post = discord.Embed()
        post.set_image(url=TAKE_A_MOMENT)
        await ctx.send(content="{0.mention} Stop, take a moment and be mindful.".format(kali),
                       embed=post)

    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def kalinocoffee(self, ctx: commands.Context):
        """
        Kali no, not the coffee
        """
        kali = ctx.bot.get_user(KALI)
        await ctx.message.add_reaction('✅')
        await kali.send(random.choice(["No Kali, don't drink the coffee",
                                       "Not with the bean juice Kali",
                                       "None Coffee - Left NoVibrate"]))

    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def kaligayy(self, ctx: commands.Context):
        """
        Kali that's gay
        """
        kali = ctx.bot.get_user(KALI)
        post = discord.Embed()
        post.set_image(url=THATS_GAY)
        await ctx.send(content="{0.mention} that's gay.".format(kali),
                       embed=post)
