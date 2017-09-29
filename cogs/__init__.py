from . import fluffy_bunnies, interact, meme, misc


def setup(bot):
    bot.add_cog(interact.Interact())
    bot.add_cog(meme.Meme())
    bot.add_cog(misc.Misc())
    bot.add_cog(fluffy_bunnies.SoulPact())
