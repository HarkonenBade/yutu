import asyncio
import datetime
import hashlib
import random
import re
import urllib.parse

import discord
from discord.ext import commands

import ao3

import html2text


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
        await ctx.send(content="**{0}** has paid {0.pronouns.dep_poss} respects {1}".format(
            ctx.author,
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

    @commands.command()
    async def quote(self, ctx: commands.Context, user: discord.Member, *, identifier=None):
        """
        Quote a user.
        
        Sends quotes to http://scarlatinashenanigans.tumblr.com
        It can only quote in the last 200 messages on channel.
        If you don't supply an identifier it will quote the users last message block.
        If you do it will quote the rest of the first block
        that starts with a message containing that text, case insensitive.
        """
        quote_user = user.name
        async for message in ctx.channel.history(limit=200, before=ctx.message):
            if message.author == user:
                if identifier is not None:
                    if identifier.lower() in message.clean_content.lower():
                        quote_text = message.clean_content
                        async for msg in ctx.channel.history(limit=100, after=message, reverse=True):
                            if msg.id == ctx.message.id or msg.author != user:
                                break
                            quote_text = quote_text + '\n' + msg.clean_content
                        break
                else:
                    quote_text = message.clean_content
                    async for msg in ctx.channel.history(limit=100, before=message):
                        if msg.author != user:
                            break
                        quote_text = msg.clean_content + '\n' + quote_text
                    break
        else:
            await ctx.send("I'm sorry, I can't find that.")
            return
        print(quote_text)
        ctx.bot.tumblr.create_quote("scarlatinashenanigans.tumblr.com",
                                    state="draft",
                                    quote=quote_text,
                                    source=quote_user)
        await ctx.send("Quoting {0.mention}:\n\"{1}\"".format(user, quote_text))

    @commands.command(hidden=True)
    async def gayformurph(self, ctx: commands.Context):
        murph = ctx.bot.get_user(184073774822326273)
        await ctx.send("{0.mention} is so very gay for {1.mention}.".format(ctx.author, murph))

    @commands.command(hidden=True)
    async def verygayformurph(self, ctx: commands.Context):
        murph = ctx.bot.get_user(184073774822326273)
        await ctx.send("Even if stranded on Themyscira, {0.mention} would swim the ocean to find {1.mention}.".format(ctx.author, murph))

    @commands.command()
    async def ao3(self, ctx: commands.Context, msg: str):
        """
        Attach a preview of an Ao3 Work
        """

        def make_link(elm):
            return "[{}]({})".format(elm,
                                     elm.url.replace("(", "%28").replace(")", "%29"))

        def make_links(lst):
            return [make_link(elm) for elm in lst]

        def make_str(lst):
            return [str(elm) for elm in lst]

        try:
            wid = int(msg)
        except ValueError:
            mtch = re.match("^https?://(?:www.)?archiveofourown.org/works/(\d*).*$", msg)
            if mtch is None:
                await ctx.send("Error: Please provide either a workID or a URL")
                return
            wid = int(mtch.group(1))
        async with ctx.typing():
            api = ao3.AO3()
            try:
                work = api.work(id=wid)
            except:
                await ctx.send("Error: Can't find a work with that ID/URL")
                return
            disp = discord.Embed()
            disp.title = work.title
            disp.url = work.url
            disp.colour = 9437184
            disp.timestamp = datetime.datetime.combine(work.published, datetime.time())
            disp.description = """
by {}

**Rating**: {}
**Archive Warnings**: {}
**Category**: {}
**Fandom**: {}
**Relationships**: {}
**Characters**: {}
**Language**: {}{}
**Stats**: Words: {} Hits: {} Kudos: {} Chapters: {}/{}

{}
            """.format(make_link(work.author),
                       ", ".join(make_str(work.rating)),
                       "No Archive Warnings Apply" if not work.warnings else ", ".join(make_str(work.warnings)),
                       ", ".join(make_str(work.category)),
                       ", ".join(make_links(work.fandoms)),
                       ", ".join(make_links(work.relationship)),
                       ", ".join(make_links(work.characters)),
                       work.language,
                       "" if work.series is None else "\n**Series**: Part {} of {}".format(work.series_idx,
                                                                                           make_link(work.series)),
                       work.words, work.hits, work.kudos,
                       work.published_chapters, "?" if work.total_chapters is None else work.total_chapters,
                       html2text.html2text(work.summary))
            await ctx.send(embed=disp)
