import asyncio
import hashlib
import random

import discord
from discord.ext import commands


class Misc:
    @commands.command()
    async def highfive(self, ctx: commands.Context):
        """
        Give Yutu a high-five
        """
        await ctx.send('{0.mention} :pray: {1.mention}'.format(ctx.me, ctx.author))

    @commands.command()
    async def rate(self, ctx: commands.Context, *, subject):
        """
        Ask Yutu to rate a thing
        """
        subject = await commands.clean_content().convert(ctx, subject)
        hasher = hashlib.sha256()
        hasher.update(subject.lower().encode("UTF-8"))
        rate = int(hasher.hexdigest(), 16) % 1001
        await ctx.e_say("**{me}** gives **{item}** a rating of **{rate}/100**",
                        item=subject,
                        rate=rate/10.0)

    @commands.command()
    async def numerology(self, ctx: commands.Context, *, subject):
        """
        Ask Yutu to do a numerology calculation on something
        """
        subject = await commands.clean_content().convert(ctx, subject)
        post = "```\nCalculating numerological result for \"{}\"\n\n".format(subject)
        chars = [c.upper() for c in subject if c.isalpha()]
        post += " + ".join(chars)
        post += "\n\n"
        vals = [((ord(c)-65) % 9) + 1 for c in chars]
        post += " + ".join([str(i) for i in vals])
        s = sum(vals)
        post += " = {}\n\n".format(s)
        while s > 9 and (s > 40 or s % 11 != 0):
            digits = [int(c) for c in str(s)]
            post += " + ".join([str(i) for i in digits])
            s = sum(digits)
            post += " = {}\n\n".format(s)
        post += "\n"
        post += {1: "1 – Initiator action, pioneering, leading, independent, attaining, individualistic",
                 2: "2 – Cooperation, adaptability, consideration of others, partnering, mediating",
                 3: "3 – Expression, verbalization, socialization, the arts, the joy of living",
                 4: "4 – Values foundation, order, service, struggle against limits, steady growth",
                 5: "5 – Expansiveness, visionary, adventure, the constructive use of freedom",
                 6: "6 – Responsibility, protection, nurturing, community, balance, sympathy",
                 7: "7 – Analysis, understanding, knowledge, awareness, studious, meditating",
                 8: "8 – Practical endeavors, status oriented, power-seeking, high-material goals",
                 9: "9 – Humanitarian, giving nature, selflessness, obligations, creative expression",
                 11: "11 – Higher spiritual plane, intuitive, illumination, idealist, a dreamer",
                 22: "22 – The Master Builder, large endeavors, powerful force, leadership",
                 33: "33 - The Master Teacher, humanitarian, usually only found in Big Names"}[s]
        post += "```"
        await ctx.send(content=post)

    @commands.command()
    async def commend(self, ctx: commands.Context, user: discord.Member, *, reason):
        """
        Commend a user, with optional reason
        """
        reason = await commands.clean_content().convert(ctx, reason)
        embed = discord.Embed()
        if reason:
            embed.description = (":trophy::military_medal: "
                                 "**{0.display_name}** commends **{1.display_name}**"
                                 " :military_medal::trophy:\n"
                                 "for {2}").format(ctx.author, user, reason)
        else:
            embed.description = (":trophy::military_medal: "
                                 "**{0.display_name}** commends **{1.display_name}**"
                                 " :military_medal::trophy:").format(ctx.author, user)
        await ctx.send(embed=embed)

    @commands.command()
    async def vote(self, ctx: commands.Context, *, msg):
        """
        Start a vote on something.
        """
        msg = await commands.clean_content().convert(ctx, msg)
        post = await ctx.send(content=":inbox_tray: A vote has been started by **{0.display_name}**".format(ctx.author),
                              embed=discord.Embed(title=msg))
        await post.add_reaction("👍")
        await post.add_reaction("🤷")
        await post.add_reaction("👎")

    @commands.command()
    async def f(self, ctx: commands.Context):
        """
        Pay your respects
        """
        await ctx.send(content="**{}** has paid {} respects {}".format(ctx.author,
                                                                       ctx.author.pronouns().dep_poss,
                                                                       random.choice([':heart:',
                                                                                      ':yellow_heart:',
                                                                                      ':blue_heart:',
                                                                                      ':purple_heart:',
                                                                                      ':green_heart:'])))

    @commands.command()
    async def poll(self, ctx: commands.Context):
        """
        Interactivly create a poll
        """
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        posts_to_del = [ctx.message, await ctx.send("Please describe the poll topic.")]

        try:
            post = await ctx.bot.wait_for("message", check=check, timeout=600)
            posts_to_del.append(post)
            topic = post.content
        except asyncio.TimeoutError:
            await ctx.send("Aborting, timed out.", delete_after=30)
            await ctx.channel.delete_messages(posts_to_del)
            return

        numerals = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣', '🔟']
        options = []
        for n in numerals:
            posts_to_del.append(await ctx.send("Please enter a poll option (max 10) or \"STOP\" to finish."))
            try:
                post = await ctx.bot.wait_for("message", check=check, timeout=600)
                posts_to_del.append(post)
                if post.content == "STOP":
                    break
                options.append((n, post.content))
            except asyncio.TimeoutError:
                await ctx.send("Aborting, timed out.", delete_after=30)
                await ctx.channel.delete_messages(posts_to_del)
                return
        await ctx.channel.delete_messages(posts_to_del)
        post = discord.Embed(description="{}\n{}".format(topic,
                                                         "\n".join(["{}: {}".format(n, option)
                                                                    for n, option in options])))
        vote = await ctx.send(content=":inbox_tray: A vote has been started by **{}**".format(ctx.author),
                              embed=post)
        for n, _ in options:
            await vote.add_reaction(n)
