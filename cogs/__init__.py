from . import fluffy_bunnies, misc

def setup(bot):
    bot.add_cog(misc.Misc())
    bot.add_cog(fluffy_bunnies.SoulPact())