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
                         description=DESCRIPTION)
        self.db = orm.Database()

    async def on_ready(self):
        print('We have logged in as {0.user}'.format(self))
        self.owner_id = (await self.application_info()).owner.id

    async def on_command_error(self, ctx: commands.Context, exception):
        if isinstance(exception, commands.errors.MissingRequiredArgument):
            for page in await self.formatter.format_help_for(ctx, ctx.command):
                await ctx.send(page)
        elif isinstance(exception, commands.CommandOnCooldown):
            await ctx.send(content=str(exception))
        else:
            await super().on_command_error(ctx, exception)
