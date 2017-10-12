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
    async def clap(self, ctx: commands.Context, *, msg):
        """
        :clap: your :clap: message :clap: here :clap:
        """
        msg = await commands.clean_content().convert(ctx, msg)
        await ctx.send(content="\n".join([":clap: " + " :clap: ".join(line.split(" ")) + " :clap:"
                                          for line in msg.split('\n')]))

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
    async def owo(self, ctx: commands.Context, *, msg):
        """
        Say something in a 'cute' way
        """
        msg = await commands.clean_content().convert(ctx, msg)
        transforms = {'na': 'nya',
                      'ne': 'nye',
                      'ni': 'nyi',
                      'nu': 'nyu',
                      'no': 'nyo',
                      'r': 'w',
                      'l': 'w'}
        for src, dst in transforms.items():
            msg = msg.replace(src, dst).replace(src.upper(), dst.upper()).replace(src.title(), dst.title())
        await ctx.send(content=msg)

    @commands.command(aliases=['leet'])
    async def l33t(self, ctx: commands.Context, *, msg):
        """
        L33t m3ss4g1ng
        """
        msg = await commands.clean_content().convert(ctx, msg)
        transforms = {'e': '3',
                      'i': '1',
                      'o': '0',
                      'a': '4',
                      's': '5',
                      'v': '\\\\/',
                      'n': '|\\\\|'}
        for src, dst in transforms.items():
            msg = msg.replace(src.lower(), dst)
        await ctx.send(content=msg)