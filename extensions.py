import discord
from discord.ext import commands

async def e_say(self: commands.Context, text: str, target: discord.Member = None, thumbnail: str = None, **kwargs):
    post = discord.Embed()
    if thumbnail is None:
        post.set_thumbnail(url=self.me.avatar_url)
    elif thumbnail != "":
        post.set_thumbnail(url=thumbnail)
    args = {'target': target,
            'author': self.message.author}
    args.update(self.__dict__)
    args.update(kwargs)
    post.description = text.format(**args)
    return await self.send(embed=post)

commands.Context.e_say = e_say

discord.Member.__str__ = lambda self: self.display_name