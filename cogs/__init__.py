from . import fluffy_bunnies, meme, misc


def setup(bot):
    bot.add_cog(meme.Meme())
    bot.add_cog(misc.Misc())
    bot.add_cog(fluffy_bunnies.SoulPact())
