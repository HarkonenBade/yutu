import discord
from discord.ext import commands
from discord.utils import get

from pony import orm


def has_roles_or_owner(*roles):
    def chk(ctx: commands.Context):
        if ctx.bot.is_owner(ctx.author):
            return True
        for role in roles:
            if get(ctx.author.roles, name=role) is not None:
                return True
        return False
    return commands.check(chk)


class Custom(commands.Cog):
    pass


class CustomCommands(commands.Cog):
    Command = None

    def __init__(self, bot: commands.Bot):
        super().__init__()
        class Command(bot.db.Entity):
            id = orm.PrimaryKey(int, auto=True)
            name = orm.Required(str)
            output_str = orm.Required(str)
            nsfw = orm.Required(bool)
            targetted = orm.Required(bool)
            help_text = orm.Required(str)
        self.Command = Command
        self.bot = bot
        bot.add_listener(self.setup, 'on_ready')

    def add_cmd(self, cmd):
        if cmd.targetted:
            async def cmd_body(_, ctx: commands.Context, target: discord.Member):
                await ctx.send(content=cmd.output_str.format(target=target,
                                                             author=ctx.author,
                                                             channel=ctx.channel))
        else:
            async def cmd_body(_, ctx: commands.Context):
                await ctx.send(content=cmd.output_str.format(author=ctx.author,
                                                             channel=ctx.channel))
        if cmd.nsfw:
            cmd_body = commands.is_nsfw()(cmd_body)
        cmd_obj = commands.command(name=cmd.name, help=cmd.help_text)(cmd_body)
        custom = self.bot.get_cog('Custom')
        setattr(custom, cmd.name, cmd_obj)
        custom.__cog_commands__.append(cmd_obj)

    async def setup(self):
        with orm.db_session:
            for cmd in orm.select(c for c in self.Command):
                self.add_cmd(cmd)

    async def get_str(self, ctx: commands.Context, preamble: str, check=lambda x: True, err='', clean=True):
        query = await ctx.send(preamble.format(ctx.author))

        def chk(msg):
            return msg.author == ctx.author and msg.channel.id == ctx.channel.id

        while True:
            msg = await ctx.bot.wait_for("message", check=chk, timeout=300)  # type: discord.Message

            if check(msg):
                await query.delete()
                await msg.delete()
                if clean:
                    return msg.clean_content
                else:
                    return msg.content
            else:
                await ctx.send(err.format(ctx.author))

    async def get_bool(self, ctx: commands.Context, preamble: str):
        def check(msg):
            return msg.clean_content.lower().strip() in ['y', 'n']
        val = await self.get_str(ctx, preamble, check, "Please choose either y or n.")
        return val.lower().strip() == "y"

    async def get_name(self, ctx: commands.Context):
        return await self.get_str(ctx,
                                  "{0.mention}: Please choose a command name, "
                                  "this is what you will type to run the command. "
                                  "Please type exactly the command you want, now.")

    async def get_nsfw(self, ctx: commands.Context):
        return await self.get_bool(ctx, "{0.mention}: Is this command NSFW? y/n?")

    async def get_targetted(self, ctx: commands.Context):
        return await self.get_bool(ctx,
                                   "{0.mention}: Is the command targetted? "
                                   "I.E. You must use it in the form `~command @someone`. y/n?")

    async def get_help(self, ctx: commands.Context):
        return await self.get_str(ctx,
                                  "{0.mention}: What should the commands help text be? "
                                  "The first line will be the short text that appears in ~help. "
                                  "The entire text will appear for ~help command. "
                                  "Please enter your help text as a single message, "
                                  "using shift+enter to add new lines.")

    async def get_invokation(self, ctx: commands.Context):
        return await self.get_str(ctx,
                                  "{0.mention}: Please enter the desired command output string. "
                                  "This is the text Yutu will post when the command is run. "
                                  "You may use the following special keywords to fill in context. "
                                  "{{author}} is the person who invoked the command. "
                                  "{{author.mention}} is the author's mention string. "
                                  "{{target}} is the target of the command if it is targetted. "
                                  "{{target.mention}} is the targets mention string. "
                                  "{{channel}} is the channel the command is invoked in. ",
                                  clean=False)

    @commands.command(name="new-custom-command", hidden=True)
    @has_roles_or_owner("mod", "owner")
    async def newcustomcommand(self, ctx: commands.Context):
        """
        Interactivly create a custom command.
        """
        with orm.db_session:
            cmd = self.Command(name=await self.get_name(ctx),
                               nsfw=await self.get_nsfw(ctx),
                               targetted=await self.get_targetted(ctx),
                               help_text=await self.get_help(ctx),
                               output_str=await self.get_invokation(ctx))
            self.add_cmd(cmd)
            await ctx.send("Ok, added the command ~{}".format(cmd.name))
