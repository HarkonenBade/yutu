from discord.ext import commands

from pony import orm


class Facts:
    Fact = None

    def __init__(self, bot: commands.Bot):
        super().__init__()
        class Fact(bot.db.Entity):
            id = orm.PrimaryKey(int, auto=True)
            text = orm.Required(str)
            author = orm.Required(str)
        self.Fact = Fact

    @commands.group(name="fact")
    async def root(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            if ctx.subcommand_passed is None:
                with orm.db_session:
                    f = self.Fact.select_random(1)
                    if len(f) == 0:
                        await ctx.send(content="We don't have any velvet facts :(")
                    else:
                        await ctx.send(content="'{}' ~{}".format(f[0].text, f[0].author))

    @root.command()
    async def add(self, ctx: commands.Context, *args):
        f = await commands.clean_content().convert(ctx, " ".join(args))
        with orm.db_session:
            self.Fact(text=f, author=str(ctx.author.mention))
        await ctx.send(content="Adding fact to database.")