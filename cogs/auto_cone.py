import asyncio
from datetime import datetime

import discord
from discord.ext import commands

from pony import orm

import dateparser
import humanize

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
            await bot.wait_until_ready()
            while True:
                with orm.db_session:
                    for val in cone.RoleRecord.select():
                        guild: discord.Guild = bot.get_guild(val.guild_id)
                        if guild is None:
                            guild = await bot.fetch_guild(val.guild_id)
                        role: discord.Role = guild.get_role(val.role_id)
                        user: discord.Member = guild.get_member(val.user_id)
                        if user is None:
                            user = await guild.fetch_member(val.user_id)

                        if role not in user.roles:
                            val.delete()
                        elif datetime.now() > val.release:
                            await user.remove_roles(role)
                            try:
                                await user.send(content=f"You have had your {role.name} role removed.")
                            finally:
                                val.delete()
                await asyncio.sleep(30)

        bot.loop.create_task(update(bot, self))

    async def meta_cone(self, ctx: commands.Context, target: discord.Member, duration: str, cone: int):
        try:
            duration = dateparser.parse(duration, settings={'PREFER_DATES_FROM': 'future',
                                                            'PREFER_DAY_OF_MONTH': 'first'})
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
                await ctx.send(content="They already have that cone until " + humanize.naturaldate(test.release))
                return
            else:
                role = ctx.guild.get_role(cone)
                self.RoleRecord(guild_id=ctx.guild.id,
                                user_id=target.id,
                                role_id=cone,
                                coner=ctx.author.id,
                                release=duration)
                await ctx.send(content="Ok, coning them until " + humanize.naturaldate(duration))
                await target.add_roles(role)

    @commands.has_role(MODS)
    @commands.command()
    async def cone(self, ctx: commands.Context, target: discord.Member, *duration):
        await self.meta_cone(ctx, target, " ".join(duration), CONE_OF_SHAME)

    @commands.has_role(MODS)
    @commands.command()
    async def uglier_cone(self, ctx: commands.Context, target: discord.Member, *duration):
        await self.meta_cone(ctx, target, " ".join(duration), UGLIER_CONE)

    @commands.has_role(MODS)
    @commands.command()
    async def birthday_cone(self, ctx: commands.Context, target: discord.Member, *duration):
        await self.meta_cone(ctx, target, " ".join(duration), BIRTHDAY_CONE)

    @commands.has_role(MODS)
    @commands.command()
    async def nv_cone(self, ctx: commands.Context, target: discord.Member, *duration):
        await self.meta_cone(ctx, target, " ".join(duration), NEW_VEGAS_CONE)

    @commands.has_role(MODS)
    @commands.command()
    async def timeout(self, ctx: commands.Context, target: discord.Member, *duration):
        await self.meta_cone(ctx, target, " ".join(duration), TIMEOUT)

    @commands.command()
    async def show_cones(self, ctx: commands.Context):
        with orm.db_session:
            embed = discord.Embed()
            embed.title = f"{ctx.author.name} Cone List"
            embed.description = ""
            for val in self.RoleRecord.select(user_id=ctx.author.id):
                guild: discord.Guild = ctx.bot.get_guild(val.guild_id)
                if guild is None:
                    guild = await ctx.bot.fetch_guild(val.guild_id)
                role: discord.Role = guild.get_role(val.role_id)
                coner: discord.Member = guild.get_member(val.coner)
                if coner is None:
                    coner = await guild.fetch_member(val.coner)
                left = val.release - datetime.now()
                left = humanize.naturaldelta(left)
                embed.description += f"Coned with **{role.name}** by *{coner.name} for {left}\n"
            await ctx.send(embed=embed)

