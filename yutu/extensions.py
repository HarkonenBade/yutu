import collections

import discord
from discord.utils import get
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

async def print_help(self: commands.Context):
    for page in await self.bot.formatter.format_help_for(self, self.command):
        await self.send(page)

commands.Context.print_help = print_help
commands.Context.e_say = e_say

discord.Member.__str__ = lambda self: self.display_name

Pronouns = collections.namedtuple("Pronouns", ['subj', 'obj', 'dep_poss', 'indep_poss'])

def pronouns(self):
    if get(self.roles, name="they/them") is not None or get(self.roles, name="they/she") is not None:
        return Pronouns('they', 'them', 'their', 'theirs')
    elif get(self.roles, name="he/him") is not None:
        return Pronouns('he', 'him', 'his', 'his')
    elif get(self.roles, name="she/her") is not None:
        return Pronouns('she', 'her', 'her', 'hers')
    elif get(self.roles, name="it/its") is not None:
        return Pronouns('it', 'it', 'its', 'its')
    elif get(self.roles, name="shark/shark") is not None:
        return Pronouns('shark', 'shark', 'sharks', 'sharks')
    return Pronouns('they', 'them', 'their', 'theirs')

discord.Member.pronouns = pronouns

class DummyArg:
    def __init__(self, name):
        self.name = name

commands.DummyArg = DummyArg
