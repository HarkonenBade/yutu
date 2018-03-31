import collections
import random

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

class s:
    def __init__(self, v):
        self.inner = v

    def __str__(self):
        return self.inner

    @property
    def cap(self):
        return self.inner.capitalize()

p_noun_map = {
    'they/them': Pronouns(s('they'), s('them'), s('their'), s('theirs')),
    'he/him': Pronouns(s('he'), s('him'), s('his'), s('his')),
    'she/her': Pronouns(s('she'), s('her'), s('her'), s('hers')),
    'it/its': Pronouns(s('it'), s('it'), s('its'), s('its'))
}

def pronouns(self):
    p = {p_noun_map[role.name] for role in self.roles if role.name in p_noun_map}
    if get(self.roles, name="they/she"):
        p.add(p_noun_map['they/them'])
        p.add(p_noun_map['she/her'])
    if get(self.roles, name="they/he"):
        p.add(p_noun_map['they/them'])
        p.add(p_noun_map['he/him'])
    if not p:
        p = {p_noun_map['they/them']}
    return random.choice(list(p))

discord.Member.pronouns = property(pronouns)

class DummyArg:
    def __init__(self, name):
        self.name = name

commands.DummyArg = DummyArg
