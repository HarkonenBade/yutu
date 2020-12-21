import os
import re
import traceback

import discord
from discord.ext import commands

from pony import orm

DESCRIPTION = """
Hi, I'm Yutu!
I'm the bot for the Velvet fan discord.
I'm still learning so sorry if I do something wrong.
You can ask my programmer @Harkonen if you want to know more about me.
"""

class Yutu(commands.Bot):
    def __init__(self):
        super().__init__(commands.when_mentioned_or("~"),
                         game=discord.Game(name="~help"),
                         description=DESCRIPTION,
                         help_command=commands.DefaultHelpCommand(dm_help=None))
        self.db = orm.Database()
        self.get_command('help').after_invoke(self.post_help)

    async def post_help(self, ctx: commands.Context):
        await ctx.message.add_reaction("✅")

    async def on_ready(self):
        print('We have logged in as {0.user}'.format(self))
        self.owner_id = (await self.application_info()).owner.id
        await self.pm_owner(content="Yutu starting up")

    async def pm_owner(self, *args, **kwargs):
        owner = self.get_user(self.owner_id)
        await owner.send(*args, **kwargs)

    async def on_command_error(self, ctx: commands.Context, exception: Exception):
        if(isinstance(exception, commands.errors.MissingRequiredArgument) or
           isinstance(exception, commands.errors.BadArgument)):
            await ctx.print_help()
        elif isinstance(exception, commands.CommandOnCooldown):
            await ctx.send(content=str(exception))
        elif isinstance(exception, commands.MissingPermissions):
            await ctx.send(content="I'm sorry {}, I can't let you do that.".format(ctx.author.mention))
        elif not isinstance(exception, commands.CommandNotFound):
            await self.pm_owner(content="".join(traceback.format_exception(None, exception, None)))
        await super().on_command_error(ctx, exception)

    async def on_message(self, message: discord.Message):
    	await super().on_message(message)
    	if message.author.id == 218548270002208768:
    		print("Rhian Message")
    		if re.match(r'\Ssex\S', message.content) is not None:
    			print("Rhian smash")
    			await message.reply(content="https://tenor.com/view/city-hunter-ryo-saeba-kaori-makimura-go-to-horny-jail-bonk-gif-18541691")

