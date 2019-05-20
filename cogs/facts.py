import discord
from discord.ext import commands

from pony import orm


class Facts(commands.Cog):
    Fact = None

    def __init__(self, bot: commands.Bot):
        super().__init__()
        class Fact(bot.db.Entity):
            id = orm.PrimaryKey(int, auto=True)
            text = orm.Required(str)
            author = orm.Required(str)
        self.Fact = Fact
        self.last_fact = 0

    @commands.group(name="fact")
    async def root(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            if ctx.subcommand_passed is None:
                with orm.db_session:
                    f = self.Fact.select_random(1)
                    if len(f) == 0:
                        await ctx.send(content="We don't have any velvet facts :(")
                    else:
                        while f[0].id == self.last_fact:
                            f = self.Fact.select_random(1)
                        self.last_fact = f[0].id
                        author = await commands.MemberConverter().convert(ctx, f[0].author)
                        await ctx.send(embed=discord.Embed(description="'{}'".format(f[0].text))
                                                    .set_author(name=author.display_name))

    @root.command()
    async def add(self, ctx: commands.Context, *, fact):
        f = await commands.clean_content().convert(ctx, fact)
        with orm.db_session:
            self.Fact(text=f, author=str(ctx.author.mention))
        await ctx.send(content="Adding fact to database.")
