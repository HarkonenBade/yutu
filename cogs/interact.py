import random

import discord
from discord.ext import commands


class Interact:
    pass


def interact_fwrk(name, text, help, aliases=[], images=None, disallow_none=False):
    @commands.command(name=name, aliases=aliases, help=help)
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
    setattr(Interact, name, cmd)


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

interact_fwrk(name='kiss',
              text='**{0.display_name}** kisses **{1.display_name}**',
              help='Kiss someone',
              aliases=['smooch'],
              disallow_none=True)
