import hashlib
import random

import discord
from discord.ext import commands


class Misc:
    @commands.command()
    async def highfive(self, ctx: commands.Context):
        """
        Give Yutu a high-five
        """
        await ctx.send('{0.mention} :pray: {1.mention}'.format(ctx.me, ctx.author))

    @commands.command()
    async def rate(self, ctx: commands.Context, *args):
        """
        Ask Yutu to rate a thing
        """
        sample = " ".join(args)
        hasher = hashlib.sha256()
        hasher.update(sample.lower().encode("UTF-8"))
        rate = int(hasher.hexdigest(), 16) % 1001
        msg = discord.Embed()
        msg.description = "**{0.display_name}** gives **{1}** a rating of **{2}/100**".format(ctx.me,
                                                                                              sample,
                                                                                              rate/10.0)
        msg.set_thumbnail(url=ctx.me.avatar_url)
        await ctx.send(embed=msg)

def interact_fwrk(name, text, help, aliases=[], images=None, disallow_none=False):
    @commands.command(name=name, aliases=aliases)
    async def cmd(self, ctx: commands.Context, user: discord.Member = None):
        if disallow_none:
            if user is None:
                await ctx.send("{0.mention}: I'm sorry I don't know that person".format(ctx.author))
                return
            else:
                first = ctx.author
                second = user
        else:
            if user is None:
                first = ctx.me
                second = ctx.author
            else:
                first = ctx.author
                second = user
        post = discord.Embed()
        if isinstance(text, list):
            post.description = random.choice(text).format(first, second)
        else:
            post.description = text.format(first, second)
        if images is not None:
            post.set_image(url=random.choice(images))
        post.set_thumbnail(url=first.avatar_url)
        await ctx.send(embed=post)
    cmd.__doc__ = help
    setattr(Misc, name, cmd)

interact_fwrk(name='cute',
              text='**{0.display_name}** thinks that **{1.display_name}** is cute!',
              help="Tell someone they are cute!",
              images=['https://i.imgur.com/MuVAkV2.gif'])

interact_fwrk(name='hug',
              text='**{0.display_name}** gives **{1.display_name}** a warm hug',
              help="Give someone a hug",
              aliases=['hugs'],
              images=['https://i.imgur.com/RDdGYgK.gif'])

interact_fwrk(name='nibble',
              text='**{0.display_name}** nibbles on **{1.display_name}**',
              help='Nibble on someone',
              aliases=['nibbles'],
              disallow_none=True)

interact_fwrk(name='pat',
              text='**{0.display_name}** pats **{1.display_name}** gently',
              help='Pat someone')

interact_fwrk(name='cuddle',
              text='**{0.display_name}** cuddles around **{1.display_name}**',
              help='Give someone a cuddle')

interact_fwrk(name='noogie',
              text='**{0.display_name}** gives **{1.display_name}** a noogie',
              help='Give someone a noogie',
              images=['https://imgur.com/a/uBOvN'],
              disallow_none=True)

interact_fwrk(name='siton',
              text='**{0.display_name}** sits down on-top of **{1.display_name}**',
              help='Sit on someone',
              aliases=['sit-on'],
              disallow_none=True)
