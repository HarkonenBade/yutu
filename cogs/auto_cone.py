import asyncio
from datetime import datetime

import discord
from discord.ext import commands

from pony import orm

import dateparser

MODS = 360515214199750658
CONE_OF_SHAME=396363935265062912
NEW_VEGAS_CONE=872544641776500747
GDI_ALY_CONE=592836652955729925
UGLIER_CONE=412401467186610177
BIRTHDAY_CONE=467707811028271104
ROWAN_CONE=576982398034640921
JADE_CONE=605105672673165346
TEST_CONE=876557119191674950
TIMEOUT=370182634535387136


class AutoCone(commands.Cog):
    RoleRecord = None

    def __init__(self, bot: commands.Bot):
        super().__init__()

        class RoleRecord(bot.db.Entity):
            id = orm.PrimaryKey(int, auto=True)
            guild_id = orm.Required(int, size=64)
            user_id = orm.Required(int, size=64)
            role_id = orm.Required(int, size=64)
            coner = orm.Required(int, size=64)
            release = orm.Required(datetime)

        self.RoleRecord = RoleRecord

        async def update(bot: commands.Bot, cone: AutoCone):
            while True:
                with orm.db_session:
                    for val in cone.RoleRecord.select(lambda v: v.release > datetime.now()):
                        guild: discord.Guild = await bot.fetch_guild(val.guild_id)
                        user: discord.Member = await guild.fetch_member(val.user_id)
                        role: discord.Role = guild.get_role(val.role_id)
                        await user.remove_roles(role)
                        try:
                            await user.send(content="You have had your f{role.name} role removed.")
                        finally:
                            val.delete()
                await asyncio.sleep(30)

        bot.loop.create_task(update(bot, self))

    async def meta_cone(self, ctx: commands.Context, target: discord.Member, duration: str, cone: int):
        try:
            duration = dateparser.parse(duration, settings={'PREFER_DATES_FROM': 'future'})
        except ValueError:
            await ctx.send(content="I'm sorry, I couldn't understand that duration, please try again.")
            return

        if duration is None:
            await ctx.send(content="I'm sorry, I couldn't understand that duration, please try again.")
            return

        if duration < datetime.now():
            await ctx.send(content="It looks like you are trying to cone them into the past, this is not permitted.")
            return

        with orm.db_session:
            test = self.RoleRecord.get(user_id=target.id, role_id=cone)
            if test is not None:
                await ctx.send(content="They already have that cone until " + str(test.release))
                return
            else:
                role = ctx.guild.get_role(cone)
                self.RoleRecord(guild_id=ctx.guild.id,
                                user_id=target.id,
                                role_id=cone,
                                coner=ctx.author.id,
                                release=duration)
                await ctx.send(content="Ok, coning them until " + str(duration))
                await target.add_roles(role)

    @commands.has_role(MODS)
    @commands.command()
    async def cone(self, ctx: commands.Context, target: discord.Member, *duration):
        await self.meta_cone(ctx, target, " ".join(duration), CONE_OF_SHAME)

    @commands.has_role(MODS)
    @commands.command()
    async def timeout(self, ctx: commands.Context, target: discord.Member, *duration):
        await self.meta_cone(ctx, target, " ".join(duration), TIMEOUT)

    @commands.command(hidden=True)
    async def show_cones(self, ctx: commands.Context):
        with orm.db_session:
            for val in self.RoleRecord.select(user_id=ctx.author.id):
                print(val.role_id)

