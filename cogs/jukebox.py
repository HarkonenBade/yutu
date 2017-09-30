import discord
from discord.ext import commands


class Jukebox:
    def __init__(self):
        self.vc = None

    @commands.command()
    async def jukebox(self, ctx: commands.Context, switch: str = None):
        post = discord.Embed()
        post.set_thumbnail(url=ctx.me.avatar_url)
        if switch is None:
            if self.vc is None:
                self.vc = await ctx.guild.voice_channels[0].connect()
                post.description = "Ok **{0.display_name}**, I'll join voice.".format(ctx.author)
            else:
                await self.vc.disconnect()
                self.vc = None
                post.description = "Ok **{0.display_name}**, I'll leave voice.".format(ctx.author)
        else:
            if switch.lower().strip() in ['on', 'yes', 'activate']:
                if self.vc is None:
                    self.vc = await ctx.guild.voice_channels[0].connect()
                    post.description = "Ok **{0.display_name}**, I'll join voice.".format(ctx.author)
                else:
                    post.description = "**{0.display_name}**, I'm already in voice chat.".format(ctx.author)
            elif switch.lower().strip() in ['off', 'no', 'deactivate']:
                if self.vc is None:
                    post.description = "**{0.display_name}**, I'm not in voice chat.".format(ctx.author)
                else:
                    await self.vc.disconnect()
                    self.vc = None
                    post.description = "Ok **{0.display_name}**, I'll leave voice.".format(ctx.author)
            else:
                post.description = "**{0.display_name}**, I don't understand that.".format(ctx.author)
        await ctx.send(embed=post)
