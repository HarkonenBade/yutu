from . import facts, fluffy_bunnies, interact, jukebox, management, meme, misc


def setup(bot):
    bot.add_cog(facts.Facts(bot))
    bot.add_cog(management.Manage())
    bot.add_cog(jukebox.Jukebox())
    bot.add_cog(interact.Interact())
    bot.add_cog(meme.Meme())
    bot.add_cog(misc.Misc())
    bot.add_cog(fluffy_bunnies.SoulPact())
