import asyncio
import random

import discord
from discord.ext import commands
from discord.utils import get
from yutu import bot

from pony import orm


class Games:
    Player = None

    def __init__(self, bot: bot.Yutu):
        super().__init__()
        class Player(bot.db.Entity):
            id = orm.PrimaryKey(int, size=64)
            coins = orm.Required(int)
        self.Player = Player

    @commands.command()
    async def fruitmachine(self, ctx: commands.Context):
        """
        Take a roll of the slots
        """
        slots = [get(ctx.guild.emojis, name='roobs'),
                 get(ctx.guild.emojis, name='wess'),
                 get(ctx.guild.emojis, name='yeng'),
                 get(ctx.guild.emojis, name='blek'),
                 get(ctx.guild.emojis, name='pyrr'),
                 get(ctx.guild.emojis, name='noodle'),
                 get(ctx.guild.emojis, name='nora'),
                 get(ctx.guild.emojis, name='renbo'),
                 get(ctx.guild.emojis, name='hapbun'),
                 get(ctx.guild.emojis, name='hapshork')]

        content = discord.Embed()

        def gen_post(player, first, second, third, under_text=None, finish=False):
            content.description = "**Welcome to Yutu's Casino {}!**\n\n".format(ctx.author)
            content.description += "**[ {} {} {} ]**\n\n".format(first, second, third)
            if under_text is not None:
                content.description += "{}\n".format(under_text)
            if player.coins == 0:
                content.description += "You are out of coins.\n\n"
            else:
                content.description += "You currently have **{}** coins.\n\n".format(player.coins)
            if finish:
                content.description += "Thank you for playing!"
            else:
                content.description += "Add a 🔁 react to spin the slots. Add ❌ to stop."
            return content

        with orm.db_session:
            await ctx.message.delete()

            try:
                player = self.Player[ctx.author.id]
            except orm.ObjectNotFound:
                player = self.Player(id=ctx.author.id, coins=10)
            gen_post(player, '❓', '❓', '❓')
            post = await ctx.send(embed=content)
            await post.add_reaction('🔁')
            await post.add_reaction('❌')

            def chk(reaction, user):
                return (str(reaction.emoji) in ['❌', '🔁'] and
                        user == ctx.author and
                        reaction.message.id == post.id)

            while True:
                if player.coins == 0:
                    break
                try:
                    react, _ = await ctx.bot.wait_for("reaction_add", check=chk, timeout=300)
                except asyncio.TimeoutError:
                    break
                if str(react.emoji) == '❌':
                    break
                player.coins -= 1
                first, second, third = random.choice(slots), random.choice(slots), random.choice(slots)

                if first == second == third:
                    player.coins += 20
                    tag = ":trophy: Jackpot! :trophy:\nYou win 20 coins!"
                elif first == second or first == third or second == third:
                    player.coins += 5
                    tag = "You win 5 coins!"
                else:
                    tag = "Better luck next time."
                gen_post(player, first, second, third, under_text=tag)
                await post.edit(embed=content)
            gen_post(player, '❓', '❓', '❓', finish=True)
            await post.edit(embed=content, delete_after=30)
